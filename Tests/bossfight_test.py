from __future__ import annotations #Resolves any possible NameErrors relating to order
import math
import sys
import time
from dataclasses import dataclass, field #Saves time instead of needing countless __init__s
from typing import Optional, Union, Callable
import random
import os
from PySide6.QtCore import QRect, QRectF, Qt, QTimer, QUrl, QPointF
from PySide6.QtGui import QColor, QFont, QKeyEvent, QPainter, QPen, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

 
class _PlayerPos:
    _instance_x: Optional[_PlayerPos] = None
    _instance_y: Optional[_PlayerPos] = None
 
    def __init__(self, axis: str) -> None:
        self._axis = axis  # "x" or "y"
 
    def __repr__(self) -> str:
        return f"PLAYER_{'X' if self._axis == 'x' else 'Y'}"
 
 
PLAYER_X: _PlayerPos = _PlayerPos("x")
PLAYER_Y: _PlayerPos = _PlayerPos("y")
 
# Type alias: any coordinate field can accept a plain float or a player pos.
Coord = Union[float, _PlayerPos]

class MusicManager:
    def __init__(self, offset_ms=0): #The improved music manager which may or may not be in the main program by the time you're reading this
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.offset = offset_ms
        self.music_list = []
        self.path = f"Program/Music/Bossfight Test"
        self.music_list = os.listdir(self.path)
        self._pending_offset = False
        self.stop_perm = False
        self.player.mediaStatusChanged.connect(self._handle_status)

    def play_random(self):
        if not self.music_list:
            return
        self.player.stop()
        self._pending_offset = self.offset > 0
        song = random.choice(self.music_list)
        self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{song}"))
        self.player.play()

    def _handle_status(self, status: QMediaPlayer.MediaStatus):
        if status == QMediaPlayer.MediaStatus.LoadedMedia or self._pending_offset:
            self._pending_offset = False
            self.player.setPosition(self.offset)
        elif status == QMediaPlayer.MediaStatus.EndOfMedia:
            if not self.stop_perm:
              self.play_random()

    def stop(self):
        self._pending_offset = False
        self.player.stop()

@dataclass
class BeamAttack:
    # axis-aligned
    orientation: str = "horizontal"
    position: Coord = 0.5

    # angled
    angle: Optional[float] = None
    origin_x: Coord = 0.5
    origin_y: Coord = 0.5

    # shared
    warning_ms: int = 1000
    duration_ms: int = 500
    thickness: int = 28
    delay_ms: int = 0
    color_warn: str = "#ffaa00"
    color_beam: str = "#ff3300"
    hitbox_shrink: int = 2
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _snapped_origin_x: Optional[float] = field(default=None, init=False)
    _snapped_origin_y: Optional[float] = field(default=None, init=False)
    _snapped_position: Optional[float] = field(default=None, init=False)
    _phase: str = field(default="waiting", init=False)
    _phase_start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)
    
@dataclass
class CircleAttack:
    x: Coord = 0.5
    y: Coord = 0.5

    # usual
    warning_ms: int = 1000
    duration_ms: int = 500
    radius: int = 28
    delay_ms: int = 0
    color_warn: str = "#ffaa00"
    color_beam: str = "#ff3300"
    hitbox_shrink: int = 2
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    _phase: str = field(default="waiting", init=False)
    _phase_start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)


@dataclass
class ProjectileAttack:
    x: float = 0.5
    y: float = 0.5
    vx: float = -0.1
    vy: float = 0.1
    size: int = 20
    delay_ms: int = 0
    image_path: Optional[str] = "Program/Assets/Low quality projectile.png" #Hard coded because going back into every single projectile instance to set the path would be tedious
    color: str = "#e040fb"
    hitbox_shrink: int = 4
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _active: bool = field(default=False, init=False)
    _done: bool = field(default=False, init=False)
    _px: float = field(default=0.0, init=False)
    _py: float = field(default=0.0, init=False)
    _pixmap: Optional[QPixmap] = field(default=None, init=False if not image_path else True)
    _fight_start: float = field(default=0.0, init=False)


@dataclass
class TextAttack:
    text: str = "..."
    x: Coord = 0.5
    y: Coord = 0.1
    duration_ms: int = 1500
    delay_ms: int = 0
    font_size: int = 32
    color: str = "#ffffff"

    # runtime state
    _active: bool = field(default=False, init=False) #I'm not going to write this on every line, but this essentially ensures that the unnecessary variables are not created on initialisation, they should not be defined on initialisastion as they are runtime states
    _done: bool = field(default=False, init=False)
    _start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    
@dataclass
class ProjectileBurst:
    '''
    A warning marker followed by projectiles that all spawn from the given location,
    if PlayerPos was used as an arugment projectiles will come from the position the player was at when the warning first appeared.

    Created with random_projectiles()
    '''
    x: Coord = 0.5
    y: Coord = 0.5
    projectiles: list[ProjectileAttack] = field(default_factory=list)
    warning_ms: int = 600
    warning_color: str = "#ff4444"
    warning_font_size: int = 18
    delay_ms: int = 0
    spawn_delay_spread_ms: int = 0

    # runtime state
    _done: bool = field(default=False, init=False)
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    _fight_start: float = field(default=0.0, init=False)

 
def rotating_beams(
    *, #Strictly keywords
    # geometry
    origin_x: float = 0.5,
    origin_y: float = 0.5,
    start_angle: float = 0.0,
    angle_between: float = 45.0,
    revolutions: float = 1.0,
    # timing
    delay_ms: int = 0,
    beam_delay_ms: int = 200,
    # BeamAttack defaults
    warning_ms: int = 1000,
    duration_ms: int = 500,
    thickness: int = 28,
    color_warn: str = "#ffaa00",
    color_beam: str = "#ff3300",
    hitbox_shrink: int = 6,
    track_player: bool= False,
    inverse: bool = False
) -> list[BeamAttack]:
    if angle_between <= 0:
        print("Angle between beams must be positive")
        return []
 
    total_degrees = 360.0 * revolutions
    raw_count = total_degrees / angle_between
    count = max(1, round(raw_count))
 
    beams: list[BeamAttack] = []
    for i in range(count):
        beams.append(BeamAttack(
            angle=start_angle + i * angle_between,
            origin_x=origin_x,
            origin_y=origin_y,
            delay_ms=delay_ms + i * beam_delay_ms,
            warning_ms=warning_ms,
            duration_ms=duration_ms,
            thickness=thickness,
            color_warn=color_warn,
            color_beam=color_beam,
            hitbox_shrink=hitbox_shrink,
            track_player=track_player,
            inverse=inverse
        ))
    return beams
def random_projectiles(
    *,
    x: Coord = 0.5,
    y: Coord = 0.5,
    amount: int = 10,
    delay_ms: int = 0,
    speed_min: float = 0.15,
    speed_max: float = 0.35,
    angle_min: float = 0.0,
    angle_max: float = 360.0,
    spawn_delay_spread_ms: int = 0,
    warning_ms: int = 600,
    warning_color: str = "#ff4444",
    warning_font_size: int = 18,
    size: int = 20,
    image_path: Optional[str] = "Program/Assets/Low quality projectile.png",
    color: str = "#e040fb",
    hitbox_shrink: int = 4,
) -> list:
    speed_min = max(speed_min, 0.05)
    speed_max = max(speed_max, speed_min)
    projectiles = []
    for i in range(amount):
        speed = random.uniform(speed_min, speed_max)
        angle_deg = random.uniform(angle_min, angle_max)
        angle_rad = math.radians(angle_deg)
        projectiles.append(ProjectileAttack(
            x=0.0, y=0.0,          # placeholder values to be overwritten
            vx=math.cos(angle_rad) * speed,
            vy=math.sin(angle_rad) * speed,
            size=size,
            delay_ms=i * spawn_delay_spread_ms,
            image_path=image_path,
            color=color,
            hitbox_shrink=hitbox_shrink,
        ))

    return [ProjectileBurst(
        x=x,
        y=y,
        projectiles=projectiles,
        warning_ms=warning_ms,
        warning_color=warning_color,
        warning_font_size=warning_font_size,
        delay_ms=delay_ms,
        spawn_delay_spread_ms=spawn_delay_spread_ms,
    )]

class BossFight(QDialog):
    """
    Fullscreen frameless PySide6 widget that runs a bullet-hell fight sequence.
 
    Parameters
    ----------
    attacks           : list of Attack Objects
    background_color  : any HEX colour string, transparency through these strings is not supported
    player_image_path : optional path to a player sprite image
    player_size       : player square side length in pixels
    player_speed      : player movement speed in pixels per second
    player_color      : fallback player colour when no image is given
    time_scale        : Speed up gameplay for debug purposes, obselete
    start_ms          : The better debug, starts from a given point in the fight
    end_ms            : Where the fight ends
    collisions_enabled: Disable collisions to test attack patterns for debugging
    end_function      : What happens when the player wins, called upon victory
    """
 
    TICK_MS = 16   # 60 fps
 
    def __init__(
        self,
        attacks: list = None,
        background_color: str = "#0d0d0d",
        player_image_path: Optional[str] = None,
        player_size: int = 28,
        player_speed: float = 280.0,
        player_color: str = "#00e5ff",
        time_scale: float = 1.0,
        start_ms: float = 0.0,
        end_ms: float = math.inf,
        collisions_enabled: bool=True,
        end_function: Optional[Callable]=None
    ):
        super().__init__()
        self._time_scale=time_scale
        self._start_ms = start_ms
        self.end_ms = end_ms
        self.end_function = end_function
        self._end_func_called = False
        self.mm = MusicManager(self._start_ms)
        self.mm.stop_perm = True
        self.collisions_enabled = collisions_enabled
 
        self._bg_color = QColor(background_color)
        self._attacks: list = attacks or []
        self._player_size = player_size
        self._player_speed = player_speed
        self._player_color = QColor(player_color)
        self._player_image_path = player_image_path
 
        # Player position
        self._player_x: float = 0.0
        self._player_y: float = 0.0
        self._keys_pressed: set[Qt.Key] = set()
 
        self._alive: bool = True
        self._victory: bool = False
        self._fight_start: float = time.monotonic()
        self._last_tick: float = self._fight_start
 
        # Load player
        self._player_pixmap: Optional[QPixmap] = None
        if player_image_path:
            pm = QPixmap(player_image_path)
            if not pm.isNull():
                self._player_pixmap = pm.scaled(
                    player_size, player_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
 
        # Preload projectile images
        now = self._fight_start
        for atk in self._attacks:
            atk._fight_start = now
            if isinstance(atk, ProjectileAttack) and atk.image_path:
                pm = QPixmap(atk.image_path)
                if not pm.isNull():
                    atk._pixmap = pm.scaled(
                        atk.size, atk.size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
            if isinstance(atk, BeamAttack):
                atk._phase = "waiting"
            if isinstance(atk, CircleAttack):
                atk._phase = "waiting"
            if isinstance(atk, ProjectileBurst):
                for projectile in atk.projectiles:
                    if projectile.image_path:
                      pm = QPixmap(projectile.image_path)
                      if not pm.isNull():
                          projectile._pixmap = pm.scaled(
                              projectile.size, projectile.size,
                              Qt.KeepAspectRatio,
                              Qt.SmoothTransformation,
                          )
        
        self._reset()
        
        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.showFullScreen()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
 
        # Game loop timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(self.TICK_MS)
 
    
    def _reset(self):
        """Reset all attack and player states so the fight can start fresh."""
        now = time.monotonic()
        self.mm.play_random()
        self._fight_start = now - self._start_ms / 1000.0
        self._last_tick = now
        self._alive = True
        self._keys_pressed.clear()
 
        # Re-centre player
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        self._player_x = cx - self._player_size / 2
        self._player_y = cy - self._player_size / 2
 
        #Reset every attack, mark any attack before start_ms as done
        for atk in self._attacks:
            atk._fight_start = now
            if isinstance(atk, BeamAttack):
                atk._phase_start = 0.0
                atk._snapped_origin_x = None
                atk._snapped_origin_y = None
                atk._snapped_position = None
                finished_by = atk.delay_ms + atk.warning_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._phase = "done"
                else:
                    atk._phase = "waiting"
            elif isinstance(atk, CircleAttack):
                atk._phase_start = 0.0
                atk._snapped_x = None
                atk._snapped_y = None
                finished_by = atk.delay_ms + atk.warning_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._phase = "done"
                else:
                    atk._phase = "waiting"
            elif isinstance(atk, ProjectileAttack):
                atk._px = 0.0
                atk._py = 0.0
                finished_by = atk.delay_ms  # projectiles go off screen and do not time out
                if finished_by <= self._start_ms:
                    # Ignore projectiles that wouldn't have spawned by this time, it is impossible to predict exact location without simulating the projectiles first
                    atk._active = False
                    atk._done = True
                else:
                    atk._active = False
                    atk._done = False
            elif isinstance(atk, TextAttack):
                atk._start = 0.0
                atk._snapped_x = None
                atk._snapped_y = None
                finished_by = atk.delay_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._active = False
                    atk._done = True
                else:
                    atk._active = False
                    atk._done = False
            elif isinstance(atk, ProjectileBurst):
                 atk._snapped_x = None
                 atk._snapped_y = None
                 last_proj_delay = max((p.delay_ms for p in atk.projectiles), default=0)
                 finished_by = atk.delay_ms + atk.warning_ms + last_proj_delay
                 atk._done = finished_by <= self._start_ms
                 for proj in atk.projectiles:
                     proj._active = False
                     proj._done = atk._done
                     proj._px = 0.0
                     proj._py = 0.0
 
    def resizeEvent(self, event):
        # Centre player on first show
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        self._player_x = cx - self._player_size / 2
        self._player_y = cy - self._player_size / 2
 
    def keyPressEvent(self, event: QKeyEvent):
       if event.key() == Qt.Key_Escape:
           self.close()
       if event.key() == Qt.Key_R and not self._alive:
           self._reset()
       if not event.isAutoRepeat():
           self._keys_pressed.add(event.key())
 
    def keyReleaseEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            self._keys_pressed.discard(event.key())

    def _tick(self):
        now = time.monotonic()
        dt = now - self._last_tick * self._time_scale
        self._last_tick = now
        elapsed_ms = (now - self._fight_start) * 1000.0 * self._time_scale
        if elapsed_ms >= self.end_ms and self._alive and not self._victory:
            self._victory = True #Funny story, I was wondering why this wasn't working, and then I realised I had put self._victory - True instead of = True
        
        if self._alive:
            self._move_player(dt)
 
        self._update_attacks(elapsed_ms, dt)
 
        if self._alive:
            self._check_collisions()
 
        self.update()  #repaint
 
    def _resolve(self, coord: Coord, axis: str) -> float:
        """
        Resolve coord to screen fraction to give player's current position
        """
        if not isinstance(coord, _PlayerPos):
            return coord
        W, H = self.width(), self.height()
        if axis == "x":
            return (self._player_x + self._player_size / 2) / W if W else 0.0
        else:
            return (self._player_y + self._player_size / 2) / H if H else 0.0
 
    def _resolve_beam_origin(self, atk: BeamAttack) -> tuple[float, float]:
        """
        Return resolved origin points, if track_player=False return player's position when attack was first called
        """
        if not atk.track_player and atk._snapped_origin_x is not None:
            return atk._snapped_origin_x, atk._snapped_origin_y
        return self._resolve(atk.origin_x, "x"), self._resolve(atk.origin_y, "y")
    def _resolve_beam_position(self, atk: BeamAttack) -> float:
        """Resolve the position on axis"""
        if not atk.track_player and atk._snapped_position is not None:
            return atk._snapped_position
        axis = "y" if atk.orientation == "horizontal" else "x"
        return self._resolve(atk.position, axis)
    def _resolve_circle_coords(self, atk: CircleAttack, W, H) -> float:
        if not atk.track_player and atk._snapped_x is not None:
            return atk._snapped_x, atk._snapped_y
        return self._resolve(atk.x, "x") * W, self._resolve(atk.y, "y") * H
 
    def _move_player(self, dt: float):
        dx = dy = 0.0
        if Qt.Key_Left in self._keys_pressed or Qt.Key_A in self._keys_pressed:
            dx -= 1
        if Qt.Key_Right in self._keys_pressed or Qt.Key_D in self._keys_pressed:
            dx += 1
        if Qt.Key_Up in self._keys_pressed or Qt.Key_W in self._keys_pressed:
            dy -= 1
        if Qt.Key_Down in self._keys_pressed or Qt.Key_S in self._keys_pressed:
            dy += 1
 
        if dx != 0 and dy != 0:
            # Diagonal movement
            factor = 0.7071
            dx *= factor
            dy *= factor
 
        speed = self._player_speed
        self._player_x += dx * speed * dt
        self._player_y += dy * speed * dt

        s = self._player_size
        self._player_x = max(0.0, min(self.width() - s, self._player_x))
        self._player_y = max(0.0, min(self.height() - s, self._player_y))
 
    def _update_attacks(self, elapsed_ms: float, dt: float):
        W, H = self.width(), self.height()
 
        for atk in self._attacks:
 
            if isinstance(atk, BeamAttack):
                if atk._phase == "waiting":
                  if elapsed_ms >= atk.delay_ms:
                      atk._phase = "warn"
                      atk._phase_start = time.monotonic()
                      if not atk.track_player:
                          atk._snapped_origin_x = self._resolve(atk.origin_x, "x")
                          atk._snapped_origin_y = self._resolve(atk.origin_y, "y")
                          # Snapshot position using the correct axis for this orientation
                          axis = "y" if atk.orientation == "horizontal" else "x"
                          atk._snapped_position = self._resolve(atk.position, axis)
                elif atk._phase == "warn":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.warning_ms:
                        atk._phase = "active"
                        atk._phase_start = time.monotonic()
                elif atk._phase == "active":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.duration_ms:
                        atk._phase = "done"
 
            elif isinstance(atk, ProjectileAttack):
                if atk._done:
                    continue
                if not atk._active:
                    if elapsed_ms >= atk.delay_ms:
                        atk._active = True
                        atk._px = self._resolve(atk.x, "x") * W
                        atk._py = self._resolve(atk.y, "y") * H
                else:
                    atk._px += atk.vx * W * dt
                    atk._py += atk.vy * H * dt
                    # End attack when off screen
                    s = atk.size
                    if (atk._px + s < 0 or atk._px > W or
                            atk._py + s < 0 or atk._py > H):
                        atk._done = True
 
            elif isinstance(atk, TextAttack):
              if atk._done:
                  continue
              if not atk._active:
                  if elapsed_ms >= atk.delay_ms:
                      atk._active = True
                      atk._snapped_x = self._resolve(atk.x, "x")
                      atk._snapped_y = self._resolve(atk.y, "y")
                      atk._start = time.monotonic()
              else:
                  age_ms = (time.monotonic() - atk._start) * 1000
                  if age_ms >= atk.duration_ms:
                      atk._done = True
            elif isinstance(atk, CircleAttack):
                W = self.width()
                H = self.height()
                if atk._phase == "waiting":
                  if elapsed_ms >= atk.delay_ms:
                      atk._phase = "warn"
                      atk._phase_start = time.monotonic()
                      if not atk.track_player:
                          atk._snapped_x, atk._snapped_y = self._resolve_circle_coords(atk, W, H)
                elif atk._phase == "warn":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.warning_ms:
                        atk._phase = "active"
                        atk._phase_start = time.monotonic()
                elif atk._phase == "active":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.duration_ms:
                        atk._phase = "done"
            elif isinstance(atk, ProjectileBurst):
                  if atk._done:
                      continue
                  elapsed_since_fight = elapsed_ms
              
                  if atk._snapped_x is None:
                      # Not triggered yet
                      if elapsed_since_fight >= atk.delay_ms:
                          atk._snapped_x = self._resolve(atk.x, "x")
                          atk._snapped_y = self._resolve(atk.y, "y")
                  else:
                      # Triggered
                      age_ms = elapsed_since_fight - atk.delay_ms
                      all_done = True
                      for proj in atk.projectiles:
                          if proj._done:
                              continue
                          all_done = False
                          proj_trigger = atk.warning_ms + proj.delay_ms
                          if not proj._active and age_ms >= proj_trigger:
                              proj._active = True
                              proj._px = atk._snapped_x * W
                              proj._py = atk._snapped_y * H
                          if proj._active:
                              proj._px += proj.vx * W * dt
                              proj._py += proj.vy * H * dt
                              s = proj.size
                              if (proj._px + s < 0 or proj._px > W or
                                      proj._py + s < 0 or proj._py > H):
                                  proj._done = True
                      if all_done and age_ms > atk.warning_ms:
                          atk._done = True
 
    def _player_hitbox(self) -> QRectF:
        """Return a slightly inset or outset hitbox for player forgiveness."""
        margin = 4
        s = self._player_size
        return QRectF(
            self._player_x + margin,
            self._player_y + margin,
            s - margin * 2,
            s - margin * 2,
        )
 
    def _check_collisions(self):
        if not self.collisions_enabled:
          return
        phb = self._player_hitbox()
 
        for atk in self._attacks:
 
            if isinstance(atk, BeamAttack):
                if atk._phase != "active":
                    continue
                sk = atk.hitbox_shrink
                t = atk.thickness
 
                if atk.angle is not None:
                    W2, H2 = self.width(), self.height()
                    ox_frac, oy_frac = self._resolve_beam_origin(atk)
                    ox = ox_frac * W2
                    oy = oy_frac * H2
                    rad = math.radians(atk.angle)
                    # Unit direction vector along the beam
                    dx = math.cos(rad)
                    dy = math.sin(rad)
                    # Player hitbox centre
                    pcx = phb.x() + phb.width() / 2
                    pcy = phb.y() + phb.height() / 2
                    # Perpendicular distance = abs(cross product of (p-o) and d) i.e. math stuff
                    rx, ry = pcx - ox, pcy - oy
                    perp_dist = abs(rx * dy - ry * dx)
                    half_hit = t / 2 - sk
                    is_colliding = perp_dist < half_hit
                    is_colliding = not is_colliding if atk.inverse else is_colliding
                    if is_colliding:
                        self._alive = False
                else:
                    W2, H2 = self.width(), self.height()
                    pos = atk.position
                    pos = self._resolve_beam_position(atk)
                    if atk.orientation == "horizontal":
                        pos = self._resolve(pos, "y")
                        cy = pos * H2
                        beam_rect = QRectF(0, cy - t / 2 + sk, W2, t - sk * 2)
                    else:
                        pos = self._resolve(pos, "x")
                        cx = pos * W2
                        beam_rect = QRectF(cx - t / 2 + sk, 0, t - sk * 2, H2)
                    is_colliding = phb.intersects(beam_rect)
                    is_colliding = not is_colliding if atk.inverse else is_colliding
                    if is_colliding:
                        self._alive = False
            elif isinstance(atk, CircleAttack):
                if atk._phase != "active":
                    continue
                sk = atk.hitbox_shrink
                W2, H2 = self.width(), self.height()
                cx, cy = self._resolve_circle_coords(atk, W2, H2)
                r = atk.radius
                closest_x = max(phb.left(), min(cx, phb.right()))
                closest_y = max(phb.top(), min(cy, phb.bottom()))
                distance_x = cx - closest_x
                distance_y = cy - closest_y
                r = r - sk
                is_colliding = (distance_x ** 2 + distance_y ** 2) < (r ** 2) #For an accurate circle the equation x^2 + y^2 < r^2 is used to check if it is within the circle. This is another math thing
                is_colliding = not is_colliding if atk.inverse else is_colliding
                if is_colliding:
                  self._alive = False
            elif isinstance(atk, ProjectileAttack):
                if not atk._active or atk._done:
                    continue
                sk = atk.hitbox_shrink
                s = atk.size
                proj_rect = QRectF(
                    atk._px + sk, atk._py + sk,
                    s - sk * 2, s - sk * 2,
                )
                is_colliding = phb.intersects(proj_rect)
                is_colliding = not is_colliding if atk.inverse else is_colliding
                if is_colliding:
                    self._alive = False
            elif isinstance(atk, ProjectileBurst):
                if atk._snapped_x is None or atk._done:
                    continue
                for proj in atk.projectiles:
                    if not proj._active or proj._done:
                        continue
                    sk = proj.hitbox_shrink
                    s = proj.size
                    proj_rect = QRectF(proj._px + sk, proj._py + sk, s - sk*2, s - sk*2)
                    if phb.intersects(proj_rect):
                        self._alive = False
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        W, H = self.width(), self.height()
        # Background
        painter.fillRect(0, 0, W, H, self._bg_color)
 
        # Draw attacks
        for atk in self._attacks:
            if isinstance(atk, CircleAttack):
                self._draw_circle(painter, atk, W, H)
            elif isinstance(atk, BeamAttack):
                self._draw_beam(painter, atk, W, H)
            elif isinstance(atk, ProjectileAttack):
                self._draw_projectile(painter, atk)
            elif isinstance(atk, TextAttack):
                self._draw_text_attack(painter, atk, W, H)
            elif isinstance(atk, ProjectileBurst):
                self._draw_burst(painter, atk, W, H)
 
        # Draw player
        self._draw_player(painter)
 
        # Death overlay
        if not self._alive:
            self._draw_death_overlay(painter, W, H)
        elif self._victory: #Skips alive check as the death overlay only applies if the player is alive and would be executed first
            self._draw_victory_overlay(painter, W, H) #Victory
 
        painter.end()
 
 
    def _beam_half_length(self, W: int, H: int) -> float:
        '''Half-diagonal of the screen'''
        return math.hypot(W, H)
 
    def _draw_beam(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        if atk._phase == "waiting" or atk._phase == "done":
            return # If the attack shouldn't be on screen don't draw it
 
        if atk.angle is not None:
            self._draw_beam_angled(painter, atk, W, H)
        else:
            self._draw_beam_axis(painter, atk, W, H)
 
    def _draw_beam_axis(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        """Axis beam drawing"""
        t = atk.thickness
        pos = atk.position
        pos = self._resolve_beam_position(atk)
 
        if atk.orientation == "horizontal":
            cy = int(pos * H)
            rect = QRect(0, cy - t // 2, W, t)
        else:
            cx = int(pos * W)
            rect = QRect(cx - t // 2, 0, t, H)
 
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            painter.fillRect(rect, color)
 
            pen = QPen(QColor(atk.color_warn))
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            if atk.orientation == "horizontal":
                painter.drawLine(0, int(pos * H), W, int(pos * H))
            else:
                painter.drawLine(int(pos * W), 0, int(pos * W), H)
 
        elif atk._phase == "active":
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            painter.fillRect(rect, color)
            core_rect = QRect(rect)
            shrink = t // 3
            if atk.orientation == "horizontal":
                core_rect.adjust(0, shrink, 0, -shrink)
            else:
                core_rect.adjust(shrink, 0, -shrink, 0)
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            painter.fillRect(core_rect, core_color)
 
    def _draw_beam_angled(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        """
        Angled beam centred on (origin_x*W, origin_y*H [for accurate relative width and heights]), rotated by "angle"
        degrees clockwise from rightward horizontal.
        """
        ox_frac, oy_frac = self._resolve_beam_origin(atk)
        ox = ox_frac * W
        oy = oy_frac * H
        half_len = self._beam_half_length(W, H)
        t = atk.thickness
 
        painter.save()
        painter.translate(ox, oy)
        painter.rotate(atk.angle)  # Rotates clockwise ofc
 
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
 
            # Warning fill
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            painter.fillRect(
                QRect(int(-half_len), -t // 2, int(half_len * 2), t),
                color,
            )
            # Dashed centre line along the beam axis, not strictly necessaru
            pen = QPen(QColor(atk.color_warn))
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(int(-half_len), 0, int(half_len), 0)
 
        elif atk._phase == "active":
            # Outer band
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            painter.fillRect(
                QRect(int(-half_len), -t // 2, int(half_len * 2), t),
                color,
            )
            #Core strip
            shrink = t // 3
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            painter.fillRect(
                QRect(int(-half_len), -t // 2 + shrink, int(half_len * 2), t - shrink * 2),
                core_color,
            )
 
        painter.restore()
    def _draw_circle(self, painter: QPainter, atk: CircleAttack, W: int, H: int):
        '''"A beam rotated on the z-axis"
            It's just a circle'''
        if atk._phase == "waiting" or atk._phase == "done":
            return #Repeat from beam code
        cx, cy = self._resolve_circle_coords(atk, W, H)
        painter.save() #Save painter settings
        painter.setPen(Qt.NoPen)
        r = atk.radius
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
 
            # Warning fill
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            brush = QBrush(color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r, r)
        elif atk._phase == "active":
            # Outer band
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            brush = QBrush(color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r, r)
            # Core
            shrink = r // 3
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            brush.setColor(core_color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r- shrink, r - shrink)
        painter.restore() #Restore painter settings to before the code altered it
 
    def _draw_projectile(self, painter: QPainter, atk: ProjectileAttack):
        if not atk._active or atk._done:
            return
        s = atk.size
        x, y = int(atk._px), int(atk._py)
        if atk._pixmap:
            painter.drawPixmap(x, y, atk._pixmap)
        else:
            color = QColor(atk.color)
            painter.fillRect(QRect(x, y, s, s), color)
            #Outline for clarity if there is no image path
            pen = QPen(QColor("#ffffff"))
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(x, y, s, s))
 
    def _draw_text_attack(self, painter: QPainter, atk: TextAttack, W: int, H: int):
        if not atk._active or atk._done:
            return
 
        age_ms = (time.monotonic() - atk._start) * 1000
        progress = age_ms / atk.duration_ms
 
        # Fade in for first 15%, fade out for last 20%, basic visuals
        if progress < 0.15:
            alpha = int(255 * (progress / 0.15))
        elif progress > 0.80:
            alpha = int(255 * (1.0 - (progress - 0.80) / 0.20))
        else:
            alpha = 255
 
        color = QColor(atk.color)
        color.setAlpha(alpha)
 
        font = QFont("Arial", atk.font_size, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(color))
 
        cx = int((atk._snapped_x if atk._snapped_x is not None else atk.x) * W)
        cy = int((atk._snapped_y if atk._snapped_y is not None else atk.y) * H)
 
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(atk.text)
        th = fm.height()
        painter.drawText(cx - tw // 2, cy + th // 3, atk.text)
    def _draw_burst(self, painter: QPainter, atk: ProjectileBurst, W: int, H: int):
        if atk._done:
            return #If it's finished return, of course
        # Draw warning dot while snapped position exists but warning is still active
        if atk._snapped_x is not None:
            elapsed_ms = (time.monotonic() - self._fight_start) * 1000.0 * self._time_scale
            age_ms = elapsed_ms - atk.delay_ms
            if age_ms < atk.warning_ms:
                progress = age_ms / atk.warning_ms
                if progress < 0.15:
                    alpha = int(255 * (progress / 0.15))
                elif progress > 0.80:
                    alpha = int(255 * (1.0 - (progress - 0.80) / 0.20))
                else:
                    alpha = 255
                color = QColor(atk.warning_color)
                color.setAlpha(alpha)
                font = QFont("Arial", atk.warning_font_size, QFont.Bold)
                painter.setFont(font)
                painter.setPen(QPen(color))
                cx = int(atk._snapped_x * W)
                cy = int(atk._snapped_y * H)
                fm = painter.fontMetrics()
                tw = fm.horizontalAdvance("●")
                th = fm.height()
                painter.drawText(cx - tw // 2, cy + th // 3, "●")
    
            # Draw active projectiles
            for proj in atk.projectiles:
                self._draw_projectile(painter, proj)
 
    def _draw_player(self, painter: QPainter):
        s = self._player_size
        x, y = int(self._player_x), int(self._player_y)
 
        if not self._alive:
            painter.setOpacity(0.35)
 
        if self._player_pixmap:
            painter.drawPixmap(x, y, self._player_pixmap)
        else:
            painter.fillRect(QRect(x, y, s, s), self._player_color)
            pen = QPen(QColor("#ffffff"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(x, y, s, s))
 
        painter.setOpacity(1.0) #Reverting opacity change incase of player death
 
    def _draw_death_overlay(self, painter: QPainter, W: int, H: int):
        overlay = QColor(180, 0, 0, 100)
        painter.fillRect(0, 0, W, H, overlay)
 
        font = QFont("Arial", 52, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#ffffff")))
        msg = "YOU DIED"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(msg)
        painter.drawText(W // 2 - tw // 2, H // 2, msg)
 
        font2 = QFont("Arial", 20)
        painter.setFont(font2)
        sub = "Press R to restart or ESC to exit"
        fm2 = painter.fontMetrics()
        tw2 = fm2.horizontalAdvance(sub)
        painter.drawText(W // 2 - tw2 // 2, H // 2 + 50, sub)
    def _draw_victory_overlay(self, painter: QPainter, W: int, H: int):
        overlay = QColor(0, 180, 0, 100)
        painter.fillRect(0, 0, W, H, overlay)
 
        font = QFont("Arial", 52, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#ffffff")))
        msg = "YOU WON"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(msg)
        painter.drawText(W // 2 - tw // 2, H // 2, msg)
 
        font2 = QFont("Arial", 20)
        painter.setFont(font2)
        sub = "Somewhere something has changed. Pressed ESC to exit."
        fm2 = painter.fontMetrics()
        tw2 = fm2.horizontalAdvance(sub)
        painter.drawText(W // 2 - tw2 // 2, H // 2 + 50, sub)
        if callable(self.end_function):
            if not self.end_func_called:
              self.end_func_called = True
              self.end_function()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    attacks = [
        TextAttack(
            text="This, will be fun.",
            x=0.5, y=0.12,
            duration_ms=1800,
            delay_ms=0,
            font_size=38,
            color="#ff0000"),
        BeamAttack(origin_x=0.35, origin_y=0.67, angle=147, warning_ms=1000, duration_ms=1500, thickness=50, delay_ms=1500, color_warn="#ff5555"),
        ProjectileAttack(0, 0, 0.5, 0.4, 50, 1500),
        ProjectileAttack(1, 0.1, -0.5, 0.4, 50, 1500),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=2500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=2.5,
            delay_ms=4500,
            beam_delay_ms=100,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0.5, y=0.5,
            amount=220,
            delay_ms=20000,
            speed_min=0.15,
            speed_max=0.60,
            spawn_delay_spread_ms=80,
            warning_ms=700,
            warning_color="#ff6644",
            size=30,
            color="#ff6644",
        ),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=70,
                        revolutions=2.5,
                        delay_ms=4500,
                        beam_delay_ms=1100,
                        warning_ms=2000,
                        duration_ms=500,
                        hitbox_shrink=6,
                        thickness=20,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=60,
                        revolutions=1.3,
                        delay_ms=20000,
                        beam_delay_ms=2500,
                        warning_ms=1000,
                        duration_ms=500,
                        hitbox_shrink=4,
                        thickness=35,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
        ProjectileAttack(1, 0.1, -0.5, 0.4, 50, 1500),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=0,
            amount=300,
            delay_ms=42000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=1,
            amount=300,
            delay_ms=42000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        TextAttack("Did you really expect it to be so easy?", 0.5, 0.1, 3000, 42000, 32, "#ff0000"),
        TextAttack("I should be insulted really...", 0.5, 0.1, 3000, 45000, 32, "#ff0000"),
        TextAttack("I'm surprised you've even lasted this long.", 0.5, 0.1, 3000, 48000, 32, "#ff0000"),
        TextAttack("But with the power your idiocy gave me...", 0.5, 0.1, 3000, 51000, 32, "#ff0000"),
        TextAttack("This is far from my limit.", 0.5, 0.1, 3000, 54000, 32, "#ff0000"),
        TextAttack("So let's make things a little more interesting.", 0.5, 0.1, 3000, 57000, 32, "#ff0000"),
        *[atk for i in range(6) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=-30.0,
            angle_between=30.0,
            revolutions=0.25,
            delay_ms=(42000 + 3000 * i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[BeamAttack(position=(0.05 + 0.1*i), orientation="vertical", warning_ms=1000, duration_ms=500, thickness=50, delay_ms=60000+(50*i), color_warn="#ff5555") for i in range(10)],
        *[BeamAttack(position=(0.05 + 0.1*i), orientation="horizontal", warning_ms=1000, duration_ms=500, thickness=50, delay_ms=60000+(50*i), color_warn="#ff5555") for i in range(10)],
        BeamAttack(position=0.5,orientation="vertical",warning_ms=1625,duration_ms=2500,thickness=750,delay_ms=60000,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_X,orientation="vertical",warning_ms=1000,duration_ms=500,thickness=100,delay_ms=69800,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_Y,orientation="horizontal",warning_ms=750,duration_ms=500,thickness=100,delay_ms=70100,color_warn="#ff5555"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=70400,
                        start_angle=0.0,
                        angle_between=21,
                        revolutions=0.6,
                        beam_delay_ms=0,
                        warning_ms=500,
                        duration_ms=1000,
                        thickness=50,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[atk for i in range(19) for atk in random_projectiles(
            x=PLAYER_X, y=PLAYER_Y,
            amount=20,
            delay_ms=62500+(1000*i),
            speed_min=0.1,
            speed_max=0.2,
            spawn_delay_spread_ms=20,
            warning_ms=1000,
            warning_color="#ff6644",
            size=15,
            color="#ff6644",
        )],
        *[atk for i in range(19) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=0.0,
            angle_between=25,
            revolutions=0.3,
            delay_ms=(62000 + 1000 * i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[atk for i in range(7) for atk in rotating_beams(
            origin_x=random.choice([0,1]),
            origin_y=random.choice([0,1]),
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=62000 + (3000*i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        BeamAttack(position=PLAYER_X,orientation="vertical",warning_ms=1000,duration_ms=500,thickness=100,delay_ms=79700,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_Y,orientation="horizontal",warning_ms=750,duration_ms=500,thickness=100,delay_ms=80100,color_warn="#ff5555"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=80500,
                        start_angle=0.0,
                        angle_between=21,
                        revolutions=0.6,
                        beam_delay_ms=0,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=50,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=80500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=80700,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
            *rotating_beams(
                origin_x=0.5,
                origin_y=0.5,
                start_angle=0.0,
                angle_between=6,
                revolutions=2.7,
                delay_ms=82700,
                beam_delay_ms=100,
                warning_ms=1000,
                duration_ms=450,
                thickness=40,
                color_warn="#ff5555",
                color_beam="#ff0000",
            ),
            *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                            delay_ms=82700,
                            start_angle=0.0,
                            angle_between=7,
                            revolutions=3.2,
                            beam_delay_ms=100,
                            warning_ms=500,
                            duration_ms=500,
                            thickness=40,
                            color_warn="#ff5555",
                            color_beam="#ff0000"),
            *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                            delay_ms=83700,
                            start_angle=0.0,
                            angle_between=7,
                            revolutions=2.8,
                            beam_delay_ms=100,
                            warning_ms=500,
                            duration_ms=500,
                            thickness=40,
                            color_warn="#ff5555",
                            color_beam="#ff0000"),
            *[atk for i in range(18) for atk in random_projectiles(
                x=PLAYER_X, y=PLAYER_Y,
                amount=15,
                delay_ms=82700+(1000*i),
                speed_min=0.1,
                speed_max=0.15,
                spawn_delay_spread_ms=20,
                warning_ms=1000,
                warning_color="#ff6644",
                size=15,
                color="#ff6644",
            )],
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=0,
            amount=300,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=1,
            amount=300,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=0,
            amount=450,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=0, y=1,
            amount=450,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *[atk for i in range(9) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=-20.0,
            angle_between=20.0,
            revolutions=0.35,
            delay_ms=(112000 + 1000 * i),
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=500,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
       TextAttack("What?", 0.5, 0.1, 3000, 102000, 32, "#ff0000"),
       TextAttack("How are you still alive?", 0.5, 0.1, 3000, 105000, 32, "#ff0000"),
       TextAttack("I'm starting to run out of assets...", 0.5, 0.1, 3000, 108000, 32, "#ff0000"),
       TextAttack("Uh...", 0.5, 0.1, 3000, 111000, 32, "#ff0000"),
       TextAttack("Pretend you didn't hear that.", 0.5, 0.1, 3000, 114000, 32, "#ff0000"),
       TextAttack("This fight is never going to end, so just give up.", 0.5, 0.1, 3000, 117000, 32, "#ff0000"),
       TextAttack("Right?", 0.5, 0.1, 3000, 120000, 32, "#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *[BeamAttack(position=PLAYER_X, orientation="vertical", warning_ms=1000, duration_ms=250, thickness=40, delay_ms=123000 + (500*i), color_warn="#ff5555", color_beam="#ff0000") for i in range(35)],
        *[BeamAttack(position=PLAYER_Y, orientation="horizontal", warning_ms=1000, duration_ms=250, thickness=40, delay_ms=123000 + (500*i), color_warn="#ff5555", color_beam="#ff0000") for i in range(35)],
        *random_projectiles(
            x=0.5, y=0.5,
            amount=200,
            delay_ms=122500,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=80,
            warning_ms=2000,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=1,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=0, y=0,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=1, y=1,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=1, y=0,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=30
        ),
        *rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=0.0,
            angle_between=21,
            revolutions=1,
            delay_ms=143000,
            beam_delay_ms=1000,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=2.8,
            delay_ms=163000,
            beam_delay_ms=100,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *[atk for i in range(12) for atk in rotating_beams(
            origin_x=random.choice([0,1]),
            origin_y=random.choice([0,1]),
            start_angle=0.0,
            angle_between=10,
            revolutions=0.5,
            delay_ms=163000+(1500*i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=500,
                       duration_ms=500,
                       delay_ms=172000 + (1000 * i),
                       radius=80,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(9)],
        TextAttack("I... don't have any more projectiles...",  0.5, 0.1, 3000, 163000, 32, "#ff0000"),
        TextAttack("I need to be a bit more creative...",  0.5, 0.1, 3000, 166000, 32, "#ff0000"),
        TextAttack("What if, I rotated the beams on the z-axis?",  0.5, 0.1, 3000, 169000, 32, "#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        CircleAttack(x=0.5, y=0.5,
                       warning_ms=1300,
                       duration_ms=38000,
                       delay_ms=181000,
                       radius=200,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                       hitbox_shrink=10),
       *rotating_beams(
                       origin_x=0.5,
                       origin_y=0.5,
                       start_angle=0.0,
                       angle_between=6,
                       revolutions=6.1,
                       delay_ms=182700,
                       beam_delay_ms=100,
                       warning_ms=1000,
                       duration_ms=450,
                       thickness=40,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                   ),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=182700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=7.2,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=183700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=6.8,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=1000,
                       duration_ms=1000,
                       delay_ms=182700 + (500*i),
                       radius=100,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(73)],
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=191200,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=201700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=211700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
                *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        TextAttack("It doesn't make any sense.",  0.5, 0.1, 3000, 222000, 32, "#ff0000"),
        TextAttack("You've survived everything I've thrown at you",  0.5, 0.1, 3000, 225000, 32, "#ff0000"),
        TextAttack("I guess I'll just have to use an attack that covers the entire fight.",  0.5, 0.1, 3000, 228000, 32, "#ff0000"),
        TextAttack("???",  0.5, 0.5, 3000, 230000, 32, "#00ff00"),
        CircleAttack(x=0.5, y=0.5,
                       warning_ms=100,
                       duration_ms=30000,
                       delay_ms=233000,
                       radius=200,
                       color_warn="#55ff55",
                       color_beam="#00ff00",
                       hitbox_shrink=-10,
                       inverse=True),
        TextAttack("What?",  0.5, 0.1, 3000, 234000, 32, "#ff0000"),
        TextAttack("Of course someone was helping you...",  0.5, 0.1, 3000, 237000, 32, "#ff0000"),
        TextAttack("I suppose I could use this to my advantage.",  0.5, 0.1, 3000, 240000, 32, "#ff0000"),
        *[atk for i in range(20) for atk in rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=30,
            revolutions=0.5,
            delay_ms=243000 + (1000*i),
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=10,
            revolutions=2.5,
            delay_ms=244000,
            beam_delay_ms=200,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=20,
            revolutions=0.5,
            delay_ms=262000,
            beam_delay_ms=50,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        TextAttack("It'll be hard to make this work...",  0.5, 0.1, 3000, 245000, 32, "#ff0000"),
        TextAttack("He seems to be preventing me from creating impossible scenarios.",  0.5, 0.1, 3000, 248000, 32, "#ff0000"),
        TextAttack("Huh, looks like there were some projectiles left over after all",  0.5, 0.1, 3000, 251000, 32, "#ff0000"),
        TextAttack("Welp, here goes something.",  0.5, 0.1, 3000, 263000, 32, "#ff0000"),
        *[atk for i in range(18) for atk in random_projectiles(
                x=PLAYER_X, y=PLAYER_Y,
                amount=15,
                delay_ms=264000+(1000*i),
                speed_min=0.1,
                speed_max=0.15,
                spawn_delay_spread_ms=20,
                warning_ms=1000,
                warning_color="#ff6644",
                size=15,
                color="#ff6644",
            )],
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=264000,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=3.5,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=1000,
                       duration_ms=1000,
                       delay_ms=264000 + (500*i),
                       radius=100,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(36)],
        *[BeamAttack(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                     angle=random.uniform(10,80),
                     warning_ms=1000,
                     duration_ms=100,
                     delay_ms=264000 + (2000*i),
                     thickness=500,
                     color_warn="#55ff55",
                     color_beam="#00ff00") for i in range(9)],
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=10,
            revolutions=3,
            delay_ms=264000,
            beam_delay_ms=175,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=3,
            delay_ms=284000,
            beam_delay_ms=100,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0.5, y=0.5,
            amount=230,
            delay_ms=284000,
            speed_min=0.15,
            speed_max=0.60,
            spawn_delay_spread_ms=80,
            warning_ms=700,
            warning_color="#ff6644",
            size=30,
            color="#ff6644",
        ),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=70,
                        revolutions=3,
                        delay_ms=284000,
                        beam_delay_ms=1100,
                        warning_ms=2000,
                        duration_ms=500,
                        hitbox_shrink=6,
                        thickness=20,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
       CircleAttack(x=0.5, y=0.5,
                       warning_ms=1000,
                       duration_ms=18200,
                       delay_ms=284000,
                       radius=200,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                       hitbox_shrink=5,
                       inverse=False),
       TextAttack("I don't understand. You survived everything I could throw at you.",  0.5, 0.1, 3000, 304000, 32, "#ff0000"),
       TextAttack("There's no more assets for me to use...",  0.5, 0.1, 3000, 307000, 32, "#ff0000"),
       TextAttack("You actually, beat me?",  0.5, 0.1, 3000, 310000, 32, "#ff0000"),
       TextAttack("I suppose you're looking for some kind of reward...",  0.5, 0.1, 3000, 313000, 32, "#ff0000"),
       TextAttack('There was some kind of "stat" in the files...',  0.5, 0.1, 3000, 316000, 32, "#ff0000"),
       TextAttack("That wasn't meant to be obtainable...",  0.5, 0.1, 3000, 319000, 32, "#ff0000"),
       TextAttack("Fine, you can have 'DENIAL', I guess you deserve it.",  0.5, 0.1, 3000, 322000, 32, "#ff0000"),
       TextAttack("I've gotta run before someone notices I'm here.",  0.5, 0.1, 3000, 325000, 32, "#ff0000"),
       TextAttack("Maybe you aren't as much of an idiot as I thought.",  0.5, 0.1, 3000, 328000, 32, "#ff0000"),
       ]

    fight = BossFight(
        attacks=attacks,
        background_color="#000000",
        player_size=20,
        player_speed=450,
        player_color="#ffffff",
        player_image_path="Program/Assets/The Culmination of Your Being.png",
        time_scale=1,
        start_ms=0,
        end_ms=344000,
        collisions_enabled=True
    )
    fight.show()
    sys.exit(app.exec())