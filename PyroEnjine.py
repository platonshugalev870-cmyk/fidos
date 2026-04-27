import pygame
import sys
import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional, Tuple, Any
import time
from collections import defaultdict


class EngineConfig:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    GRAVITY = 0.5
    DT_FIXED = 1.0 / 60.0
    MAX_PARTICLES = 5000
    SOUND_ENABLED = True


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        l = self.length()
        if l > 0:
            return Vector2(self.x / l, self.y / l)
        return Vector2(0, 0)
    
    def copy(self):
        return Vector2(self.x, self.y)


class Transform:
    def __init__(self, position: Vector2 = None, rotation: float = 0, scale: Vector2 = None):
        self.position = position or Vector2(0, 0)
        self.rotation = rotation
        self.scale = scale or Vector2(1, 1)
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def world_position(self):
        if self.parent:
            return self.parent.world_position() + self.position
        return self.position


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)


class CollisionLayer(Enum):
    DEFAULT = 1
    PLAYER = 2
    ENEMY = 4
    PROJECTILE = 8
    POWERUP = 16
    WALL = 32
    TRIGGER = 64


@dataclass
class CollisionInfo:
    point: Vector2
    normal: Vector2
    penetration: float
    other: 'GameObject'


class Component:
    def __init__(self, game_object: 'GameObject'):
        self.game_object = game_object
        self.enabled = True
    
    def start(self):
        pass
    
    def update(self, dt: float):
        pass
    
    def fixed_update(self, dt: float):
        pass
    
    def late_update(self, dt: float):
        pass
    
    def on_collision_enter(self, other: 'GameObject', collision: CollisionInfo):
        pass
    
    def on_collision_exit(self, other: 'GameObject'):
        pass
    
    def on_trigger_enter(self, other: 'GameObject'):
        pass


class GameObject:
    def __init__(self, name: str = "GameObject"):
        self.name = name
        self.transform = Transform()
        self.components: List[Component] = []
        self.is_active = True
        self.tag = ""
        self.layer = CollisionLayer.DEFAULT
        self.rigidbody: Optional['Rigidbody'] = None
        self.collider: Optional['Collider'] = None
    
    def add_component(self, component: Component):
        self.components.append(component)
        return component
    
    def get_component(self, component_type):
        for comp in self.components:
            if isinstance(comp, component_type):
                return comp
        return None
    
    def start(self):
        for comp in self.components:
            comp.start()
    
    def update(self, dt: float):
        if not self.is_active:
            return
        for comp in self.components:
            if comp.enabled:
                comp.update(dt)
    
    def fixed_update(self, dt: float):
        if not self.is_active:
            return
        for comp in self.components:
            if comp.enabled:
                comp.fixed_update(dt)
    
    def late_update(self, dt: float):
        if not self.is_active:
            return
        for comp in self.components:
            if comp.enabled:
                comp.late_update(dt)
    
    def destroy(self):
        Engine.get_instance().destroy_object(self)


class Rigidbody(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.velocity = Vector2(0, 0)
        self.angular_velocity = 0
        self.mass = 1.0
        self.is_kinematic = False
        self.use_gravity = True
        self.drag = 0.98
        self.angular_drag = 0.98
        self.gravity_scale = 1.0
    
    def add_force(self, force: Vector2, force_mode: str = "Force"):
        if not self.is_kinematic:
            acceleration = force / self.mass
            self.velocity += acceleration
    
    def fixed_update(self, dt: float):
        if self.is_kinematic:
            return
        
        if self.use_gravity:
            self.velocity.y += EngineConfig.GRAVITY * self.gravity_scale * dt
        
        self.velocity *= self.drag
        self.angular_velocity *= self.angular_drag
        
        self.game_object.transform.position += self.velocity * dt
        self.game_object.transform.rotation += self.angular_velocity * dt


class Collider(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.is_trigger = False
        self.offset = Vector2(0, 0)
    
    def world_bounds(self):
        pos = self.game_object.transform.world_position() + self.offset
        return pos
    
    def check_collision(self, other: 'Collider') -> Optional[CollisionInfo]:
        return None


class BoxCollider(Collider):
    def __init__(self, game_object: GameObject, width: float, height: float):
        super().__init__(game_object)
        self.width = width
        self.height = height
    
    def world_bounds(self):
        pos = super().world_bounds()
        scale = self.game_object.transform.scale
        return (pos.x - self.width * scale.x / 2,
                pos.y - self.height * scale.y / 2,
                self.width * scale.x,
                self.height * scale.y)
    
    def check_collision(self, other: Collider) -> Optional[CollisionInfo]:
        if isinstance(other, BoxCollider):
            return self.check_box_box(self, other)
        elif isinstance(other, CircleCollider):
            return self.check_box_circle(self, other)
        return None
    
    @staticmethod
    def check_box_box(a: 'BoxCollider', b: 'BoxCollider') -> Optional[CollisionInfo]:
        ax, ay, aw, ah = a.world_bounds()
        bx, by, bw, bh = b.world_bounds()
        
        if ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by:
            overlap_x = min(ax + aw - bx, bx + bw - ax)
            overlap_y = min(ay + ah - by, by + bh - ay)
            
            if overlap_x < overlap_y:
                normal = Vector2(1 if ax < bx else -1, 0)
                penetration = overlap_x
            else:
                normal = Vector2(0, 1 if ay < by else -1)
                penetration = overlap_y
            
            return CollisionInfo(
                point=Vector2(max(ax, bx), max(ay, by)),
                normal=normal,
                penetration=penetration,
                other=b.game_object
            )
        return None
    
    @staticmethod
    def check_box_circle(box: 'BoxCollider', circle: 'CircleCollider') -> Optional[CollisionInfo]:
        closest_x = max(box.world_bounds()[0], min(circle.world_center().x, box.world_bounds()[0] + box.world_bounds()[2]))
        closest_y = max(box.world_bounds()[1], min(circle.world_center().y, box.world_bounds()[1] + box.world_bounds()[3]))
        
        dx = circle.world_center().x - closest_x
        dy = circle.world_center().y - closest_y
        
        if dx * dx + dy * dy < circle.radius * circle.radius:
            return CollisionInfo(
                point=Vector2(closest_x, closest_y),
                normal=Vector2(dx, dy).normalize(),
                penetration=circle.radius - math.sqrt(dx*dx + dy*dy),
                other=circle.game_object
            )
        return None


class CircleCollider(Collider):
    def __init__(self, game_object: GameObject, radius: float):
        super().__init__(game_object)
        self.radius = radius
    
    def world_center(self):
        return super().world_bounds()
    
    def check_collision(self, other: Collider) -> Optional[CollisionInfo]:
        if isinstance(other, CircleCollider):
            return self.check_circle_circle(self, other)
        elif isinstance(other, BoxCollider):
            return BoxCollider.check_box_circle(other, self)
        return None
    
    @staticmethod
    def check_circle_circle(a: 'CircleCollider', b: 'CircleCollider') -> Optional[CollisionInfo]:
        delta = a.world_center() - b.world_center()
        distance = delta.length()
        radius_sum = a.radius + b.radius
        
        if distance < radius_sum:
            return CollisionInfo(
                point=a.world_center() + delta.normalize() * a.radius,
                normal=delta.normalize(),
                penetration=radius_sum - distance,
                other=b.game_object
            )
        return None


class SpriteRenderer(Component):
    def __init__(self, game_object: GameObject, color: Tuple[int, int, int] = Color.WHITE, size: Vector2 = None):
        super().__init__(game_object)
        self.color = color
        self.size = size or Vector2(32, 32)
        self.texture = None
    
    def update(self, dt: float):
        pass


class Animator(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.animations: Dict[str, 'Animation'] = {}
        self.current_animation: Optional['Animation'] = None
        self.current_time = 0
        self.loop = True
        self.paused = False
    
    def add_animation(self, name: str, animation: 'Animation'):
        self.animations[name] = animation
    
    def play(self, name: str, loop: bool = True):
        if name in self.animations and self.current_animation != self.animations[name]:
            self.current_animation = self.animations[name]
            self.current_time = 0
            self.loop = loop
    
    def update(self, dt: float):
        if not self.current_animation or self.paused:
            return
        
        self.current_time += dt
        if self.current_time >= self.current_animation.duration:
            if self.loop:
                self.current_time = 0
            else:
                self.current_time = self.current_animation.duration
    
    def current_frame(self):
        if not self.current_animation:
            return 0
        return int((self.current_time / self.current_animation.duration) * len(self.current_animation.frames))


class Animation:
    def __init__(self, frames: List[Any], duration: float = 1.0):
        self.frames = frames
        self.duration = duration


class ParticleSystem(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.particles: List['Particle'] = []
        self.emission_rate = 50
        self.emission_timer = 0
        self.particle_lifetime = 1.0
        self.particle_speed = 100
        self.particle_size = 4
        self.particle_color = Color.WHITE
        self.gravity_effect = 0
    
    def update(self, dt: float):
        self.emission_timer += dt
        particles_to_emit = int(self.emission_timer * self.emission_rate)
        
        for _ in range(particles_to_emit):
            if len(self.particles) < EngineConfig.MAX_PARTICLES:
                self.emit_particle()
        
        self.emission_timer -= particles_to_emit / self.emission_rate
        
        for particle in self.particles[:]:
            particle.life -= dt
            if particle.life <= 0:
                self.particles.remove(particle)
                continue
            
            particle.velocity.y += self.gravity_effect * dt
            particle.position += particle.velocity * dt
            particle.size = self.particle_size * (1 - particle.life / self.particle_lifetime)
    
    def emit_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5) * self.particle_speed
        velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        
        self.particles.append(Particle(
            position=self.game_object.transform.position.copy(),
            velocity=velocity,
            life=self.particle_lifetime,
            size=self.particle_size,
            color=self.particle_color
        ))
    
    def render(self, screen):
        for particle in self.particles:
            alpha = int(255 * (1 - particle.life / self.particle_lifetime))
            color = (*particle.color[:3], alpha)
            pygame.draw.circle(screen, particle.color[:3], 
                              (int(particle.position.x), int(particle.position.y)), 
                              int(particle.size))


class Particle:
    def __init__(self, position: Vector2, velocity: Vector2, life: float, size: float, color: Tuple):
        self.position = position
        self.velocity = velocity
        self.life = life
        self.size = size
        self.color = color


class Camera:
    def __init__(self):
        self.transform = Transform()
        self.zoom = 1.0
        self.follow_target: Optional[GameObject] = None
        self.follow_speed = 5.0
    
    def update(self, dt: float):
        if self.follow_target:
            target_pos = self.follow_target.transform.world_position()
            self.transform.position.x += (target_pos.x - self.transform.position.x) * self.follow_speed * dt
            self.transform.position.y += (target_pos.y - self.transform.position.y) * self.follow_speed * dt
    
    def world_to_screen(self, world_pos: Vector2, screen_size: Vector2) -> Vector2:
        screen_x = (world_pos.x - self.transform.position.x) * self.zoom + screen_size.x / 2
        screen_y = (world_pos.y - self.transform.position.y) * self.zoom + screen_size.y / 2
        return Vector2(screen_x, screen_y)
    
    def screen_to_world(self, screen_pos: Vector2, screen_size: Vector2) -> Vector2:
        world_x = (screen_pos.x - screen_size.x / 2) / self.zoom + self.transform.position.x
        world_y = (screen_pos.y - screen_size.y / 2) / self.zoom + self.transform.position.y
        return Vector2(world_x, world_y)


class Scene:
    def __init__(self, name: str):
        self.name = name
        self.game_objects: List[GameObject] = []
        self.game_objects_to_add: List[GameObject] = []
        self.game_objects_to_remove: List[GameObject] = []
        self.camera = Camera()
        self.background_color = Color.BLACK
    
    def add_game_object(self, obj: GameObject):
        self.game_objects_to_add.append(obj)
    
    def remove_game_object(self, obj: GameObject):
        self.game_objects_to_remove.append(obj)
    
    def start(self):
        for obj in self.game_objects:
            obj.start()
    
    def update(self, dt: float):
        for obj in self.game_objects_to_add:
            self.game_objects.append(obj)
            obj.start()
        self.game_objects_to_add.clear()
        
        for obj in self.game_objects_to_remove:
            if obj in self.game_objects:
                self.game_objects.remove(obj)
        self.game_objects_to_remove.clear()
        
        for obj in self.game_objects:
            obj.update(dt)
        
        self.camera.update(dt)
    
    def fixed_update(self, dt: float):
        for obj in self.game_objects:
            obj.fixed_update(dt)
    
    def late_update(self, dt: float):
        for obj in self.game_objects:
            obj.late_update(dt)
    
    def render(self, screen):
        screen.fill(self.background_color)
        
        for obj in self.game_objects:
            sprite = obj.get_component(SpriteRenderer)
            if sprite:
                world_pos = obj.transform.world_position()
                screen_pos = self.camera.world_to_screen(world_pos, Vector2(EngineConfig.WIDTH, EngineConfig.HEIGHT))
                
                rect = pygame.Rect(screen_pos.x - sprite.size.x * self.camera.zoom / 2,
                                  screen_pos.y - sprite.size.y * self.camera.zoom / 2,
                                  sprite.size.x * self.camera.zoom,
                                  sprite.size.y * self.camera.zoom)
                pygame.draw.rect(screen, sprite.color, rect)
                
                if obj.get_component(BoxCollider) and False:
                    pygame.draw.rect(screen, Color.RED, rect, 2)
            
            particle_system = obj.get_component(ParticleSystem)
            if particle_system:
                particle_system.render(screen)


class PhysicsSystem:
    def __init__(self):
        self.collision_pairs = set()
    
    def update(self, scene: Scene, dt: float):
        colliders = []
        for obj in scene.game_objects:
            if obj.collider and obj.is_active:
                colliders.append(obj)
        
        for i, obj_a in enumerate(colliders):
            for obj_b in colliders[i+1:]:
                if not (obj_a.collider and obj_b.collider):
                    continue
                
                if (obj_a.layer.value & obj_b.layer.value) == 0 and obj_a.layer != CollisionLayer.DEFAULT:
                    continue
                
                collision = obj_a.collider.check_collision(obj_b.collider)
                
                pair_key = (min(id(obj_a), id(obj_b)), max(id(obj_a), id(obj_b)))
                
                if collision:
                    if pair_key not in self.collision_pairs:
                        obj_a.on_collision_enter(obj_b, collision)
                        obj_b.on_collision_enter(obj_a, collision)
                        self.collision_pairs.add(pair_key)
                    
                    if not obj_a.collider.is_trigger and not obj_b.collider.is_trigger:
                        self.resolve_collision(obj_a, obj_b, collision)
                else:
                    if pair_key in self.collision_pairs:
                        obj_a.on_collision_exit(obj_b)
                        obj_b.on_collision_exit(obj_a)
                        self.collision_pairs.remove(pair_key)
    
    def resolve_collision(self, obj_a: GameObject, obj_b: GameObject, collision: CollisionInfo):
        rb_a = obj_a.rigidbody
        rb_b = obj_b.rigidbody
        
        if not rb_a and not rb_b:
            return
        
        if rb_a and not rb_b:
            rb_a.velocity = Vector2(0, 0)
            obj_a.transform.position -= collision.normal * collision.penetration
        elif not rb_a and rb_b:
            rb_b.velocity = Vector2(0, 0)
            obj_b.transform.position += collision.normal * collision.penetration
        else:
            total_mass = rb_a.mass + rb_b.mass
            if total_mass > 0:
                correction = collision.normal * (collision.penetration / 2)
                obj_a.transform.position -= correction
                obj_b.transform.position += correction
                
                relative_velocity = rb_a.velocity - rb_b.velocity
                velocity_along_normal = relative_velocity.dot(collision.normal)
                
                if velocity_along_normal < 0:
                    restitution = 0.5
                    impulse = -(1 + restitution) * velocity_along_normal
                    impulse /= (1/rb_a.mass + 1/rb_b.mass)
                    
                    rb_a.velocity -= collision.normal * (impulse / rb_a.mass)
                    rb_b.velocity += collision.normal * (impulse / rb_b.mass)


class Input:
    _keys_pressed = set()
    _keys_just_pressed = set()
    _keys_just_released = set()
    _mouse_pos = Vector2(0, 0)
    _mouse_buttons = set()
    _mouse_buttons_just_pressed = set()
    
    @classmethod
    def update(cls):
        cls._keys_just_pressed.clear()
        cls._keys_just_released.clear()
        cls._mouse_buttons_just_pressed.clear()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                cls._keys_pressed.add(event.key)
                cls._keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                cls._keys_pressed.discard(event.key)
                cls._keys_just_released.add(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cls._mouse_buttons.add(event.button)
                cls._mouse_buttons_just_pressed.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                cls._mouse_buttons.discard(event.button)
            elif event.type == pygame.MOUSEMOTION:
                cls._mouse_pos = Vector2(event.pos[0], event.pos[1])
        
        return True
    
    @classmethod
    def get_key(cls, key):
        return key in cls._keys_pressed
    
    @classmethod
    def get_key_down(cls, key):
        return key in cls._keys_just_pressed
    
    @classmethod
    def get_key_up(cls, key):
        return key in cls._keys_just_released
    
    @classmethod
    def get_mouse_position(cls):
        return cls._mouse_pos
    
    @classmethod
    def get_mouse_button(cls, button):
        return button in cls._mouse_buttons
    
    @classmethod
    def get_mouse_button_down(cls, button):
        return button in cls._mouse_buttons_just_pressed


class AudioSource(Component):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.sounds = {}
    
    def load_sound(self, name: str, path: str):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except:
            pass
    
    def play(self, name: str, loops: int = 0):
        if name in self.sounds:
            self.sounds[name].play(loops)
    
    def stop(self, name: str):
        if name in self.sounds:
            self.sounds[name].stop()


class Engine:
    _instance: Optional['Engine'] = None
    
    @classmethod
    def get_instance(cls):
        return cls._instance
    
    def __init__(self):
        Engine._instance = self
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((EngineConfig.WIDTH, EngineConfig.HEIGHT))
        pygame.display.set_caption("Game Engine - Python Edition")
        self.clock = pygame.time.Clock()
        
        self.current_scene: Optional[Scene] = None
        self.scenes: Dict[str, Scene] = {}
        self.physics = PhysicsSystem()
        self.running = True
        self.delta_time = 0
        self.fixed_time_accumulator = 0
    
    def add_scene(self, scene: Scene):
        self.scenes[scene.name] = scene
        if not self.current_scene:
            self.current_scene = scene
            scene.start()
    
    def load_scene(self, name: str):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            self.current_scene.start()
    
    def destroy_object(self, obj: GameObject):
        if self.current_scene:
            self.current_scene.remove_game_object(obj)
    
    def instantiate(self, obj: GameObject):
        if self.current_scene:
            self.current_scene.add_game_object(obj)
    
    def run(self):
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = min(current_time - last_time, 0.033)
            last_time = current_time
            
            if not Input.update():
                self.running = False
                break
            
            self.fixed_time_accumulator += dt
            while self.fixed_time_accumulator >= EngineConfig.DT_FIXED:
                if self.current_scene:
                    self.current_scene.fixed_update(EngineConfig.DT_FIXED)
                    self.physics.update(self.current_scene, EngineConfig.DT_FIXED)
                self.fixed_time_accumulator -= EngineConfig.DT_FIXED
            
            if self.current_scene:
                self.current_scene.update(dt)
                self.current_scene.late_update(dt)
                self.current_scene.render(self.screen)
            
            pygame.display.flip()
            self.delta_time = self.clock.tick(EngineConfig.FPS) / 1000.0
        
        pygame.quit()
        sys.exit()


class SamplePlayerController(Component):
    def __init__(self, game_object: GameObject, speed: float = 300):
        super().__init__(game_object)
        self.speed = speed
    
    def update(self, dt: float):
        rb = self.game_object.rigidbody
        if not rb:
            return
        
        move = Vector2(0, 0)
        if Input.get_key(pygame.K_LEFT) or Input.get_key(pygame.K_a):
            move.x = -1
        if Input.get_key(pygame.K_RIGHT) or Input.get_key(pygame.K_d):
            move.x = 1
        if Input.get_key(pygame.K_UP) or Input.get_key(pygame.K_w):
            move.y = -1
        if Input.get_key(pygame.K_DOWN) or Input.get_key(pygame.K_s):
            move.y = 1
        
        rb.add_force(move.normalize() * self.speed)
        
        if Input.get_key_down(pygame.K_SPACE):
            self.jump()
    
    def jump(self):
        rb = self.game_object.rigidbody
        if rb and abs(rb.velocity.y) < 0.1:
            rb.add_force(Vector2(0, -400))


class EnemyAI(Component):
    def __init__(self, game_object: GameObject, speed: float = 100, detection_range: float = 300):
        super().__init__(game_object)
        self.speed = speed
        self.detection_range = detection_range
        self.player: Optional[GameObject] = None
    
    def start(self):
        for obj in Engine.get_instance().current_scene.game_objects:
            if obj.tag == "Player":
                self.player = obj
                break
    
    def update(self, dt: float):
        if not self.player:
            return
        
        rb = self.game_object.rigidbody
        if not rb:
            return
        
        direction = self.player.transform.position - self.game_object.transform.position
        
        if direction.length() < self.detection_range:
            rb.add_force(direction.normalize() * self.speed)


class HealthSystem(Component):
    def __init__(self, game_object: GameObject, max_health: float = 100):
        super().__init__(game_object)
        self.max_health = max_health
        self.current_health = max_health
        self.on_death: Optional[Callable] = None
        self.on_damage: Optional[Callable] = None
    
    def damage(self, amount: float):
        self.current_health -= amount
        if self.on_damage:
            self.on_damage(amount)
        
        if self.current_health <= 0:
            self.die()
    
    def heal(self, amount: float):
        self.current_health = min(self.current_health + amount, self.max_health)
    
    def die(self):
        if self.on_death:
            self.on_death()
        self.game_object.destroy()


class SampleGameScene(Scene):
    def __init__(self):
        super().__init__("SampleScene")
        self.background_color = Color.DARK_GRAY
    
    def start(self):
        player = GameObject("Player")
        player.tag = "Player"
        player.transform.position = Vector2(EngineConfig.WIDTH / 2, EngineConfig.HEIGHT / 2)
        
        rb = player.add_component(Rigidbody(player))
        rb.mass = 10
        
        collider = player.add_component(BoxCollider(player, 40, 40))
        player.collider = collider
        
        sprite = player.add_component(SpriteRenderer(player, Color.CYAN, Vector2(40, 40)))
        
        controller = player.add_component(SamplePlayerController(player, 500))
        
        health = player.add_component(HealthSystem(player, 100))
        
        particle = player.add_component(ParticleSystem(player))
        particle.emission_rate = 20
        particle.particle_color = Color.CYAN
        
        self.add_game_object(player)
        
        for i in range(5):
            enemy = GameObject(f"Enemy_{i}")
            enemy.tag = "Enemy"
            enemy.transform.position = Vector2(random.randint(100, EngineConfig.WIDTH - 100),
                                               random.randint(100, EngineConfig.HEIGHT - 100))
            
            rb_e = enemy.add_component(Rigidbody(enemy))
            rb_e.mass = 5
            
            collider_e = enemy.add_component(BoxCollider(enemy, 35, 35))
            enemy.collider = collider_e
            
            sprite_e = enemy.add_component(SpriteRenderer(enemy, Color.RED, Vector2(35, 35)))
            
            ai = enemy.add_component(EnemyAI(enemy, 150, 350))
            
            health_e = enemy.add_component(HealthSystem(enemy, 50))
            
            self.add_game_object(enemy)
        
        wall_left = GameObject("WallLeft")
        wall_left.transform.position = Vector2(-50, EngineConfig.HEIGHT / 2)
        rb_w = wall_left.add_component(Rigidbody(wall_left))
        rb_w.is_kinematic = True
        collider_w = wall_left.add_component(BoxCollider(wall_left, 50, EngineConfig.HEIGHT))
        wall_left.collider = collider_w
        self.add_game_object(wall_left)
        
        wall_right = GameObject("WallRight")
        wall_right.transform.position = Vector2(EngineConfig.WIDTH + 50, EngineConfig.HEIGHT / 2)
        rb_w2 = wall_right.add_component(Rigidbody(wall_right))
        rb_w2.is_kinematic = True
        collider_w2 = wall_right.add_component(BoxCollider(wall_right, 50, EngineConfig.HEIGHT))
        wall_right.collider = collider_w2
        self.add_game_object(wall_right)
        
        wall_top = GameObject("WallTop")
        wall_top.transform.position = Vector2(EngineConfig.WIDTH / 2, -50)
        rb_w3 = wall_top.add_component(Rigidbody(wall_top))
        rb_w3.is_kinematic = True
        collider_w3 = wall_top.add_component(BoxCollider(wall_top, EngineConfig.WIDTH, 50))
        wall_top.collider = collider_w3
        self.add_game_object(wall_top)
        
        wall_bottom = GameObject("WallBottom")
        wall_bottom.transform.position = Vector2(EngineConfig.WIDTH / 2, EngineConfig.HEIGHT + 50)
        rb_w4 = wall_bottom.add_component(Rigidbody(wall_bottom))
        rb_w4.is_kinematic = True
        collider_w4 = wall_bottom.add_component(BoxCollider(wall_bottom, EngineConfig.WIDTH, 50))
        wall_bottom.collider = collider_w4
        self.add_game_object(wall_bottom)
        
        self.camera.follow_target = player
        self.camera.follow_speed = 8


class UIText(Component):
    def __init__(self, game_object: GameObject, text: str = "", color: Tuple = Color.WHITE, font_size: int = 24):
        super().__init__(game_object)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
    
    def update(self, dt: float):
        screen = Engine.get_instance().screen
        rendered = self.font.render(self.text, True, self.color)
        screen.blit(rendered, (int(self.game_object.transform.position.x), int(self.game_object.transform.position.y)))


def main():
    engine = Engine()
    
    game_scene = SampleGameScene()
    engine.add_scene(game_scene)
    
    engine.run()


if __name__ == "__main__":
    main()
