import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


"""
CONTROLES
--------------------------
TAB / 1–5  -> Cambiar modelo enfocado
H          -> Cambiar shader
R          -> Reset shaders

Z / X      -> Aumentar y reducir animación 

Mouse drag / flechas derecha e izquierda -> Orbitar 
Mouse wheel / flechas arriba y abajo -> Zoom

W / S      -> Subir y bajar 
Q / E      -> Ajustar elevación
"""



width = 960
height = 540

deltaTime = 0.0

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.pointLight = glm.vec3(0, 5, 0)

skyboxTextures = ["skybox/cube_left.png",
				  "skybox/cube_right.png",
				  "skybox/cube_up.png",
				  "skybox/cube_down.png",
				  "skybox/cube_front.png",
				  "skybox/cube_back.png"]

rend.CreateSkybox(skyboxTextures)

class ModelShaderConfig:
    def __init__(self, model, name, position, shaderPresets):
        self.model = model
        self.name = name
        self.position = position
        self.currentPreset = 0
        self.shaderPresets = shaderPresets
        self.shader = None
        self.compileCurrentShader()
    
    def compileCurrentShader(self):
        vertexSource, fragmentSource = self.shaderPresets[self.currentPreset]
        
        if vertexSource is not None and fragmentSource is not None:
            self.shader = compileProgram(
                compileShader(vertexSource, GL_VERTEX_SHADER),
                compileShader(fragmentSource, GL_FRAGMENT_SHADER)
            )
    
    def nextPreset(self):
        self.currentPreset = (self.currentPreset + 1) % len(self.shaderPresets)
        self.compileCurrentShader()
    
    def useShader(self, camera, pointLight, ambientLight, elapsedTime, value):
        if self.shader is not None:
            glUseProgram(self.shader)
            
            glUniformMatrix4fv(glGetUniformLocation(self.shader, "viewMatrix"),
                              1, GL_FALSE, glm.value_ptr(camera.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.shader, "projectionMatrix"),
                              1, GL_FALSE, glm.value_ptr(camera.projectionMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.shader, "modelMatrix"),
                              1, GL_FALSE, glm.value_ptr(self.model.GetModelMatrix()))
            
            glUniform3fv(glGetUniformLocation(self.shader, "pointLight"), 1, glm.value_ptr(pointLight))
            glUniform1f(glGetUniformLocation(self.shader, "ambientLight"), ambientLight)
            
            glUniform1f(glGetUniformLocation(self.shader, "time"), elapsedTime)
            glUniform1f(glGetUniformLocation(self.shader, "value"), value)
            
            glUniform1i(glGetUniformLocation(self.shader, "tex0"), 0)
            glUniform1i(glGetUniformLocation(self.shader, "tex1"), 1)

penguin = Model("models/Penguin.obj")
penguin.AddTexture("textures/Penguin.bmp")
penguin.position.z = -5
penguin.position.y = -0.8
penguin.position.x = 1
penguin.visible = True

bird = Model("models/bird.obj")
bird.AddTexture("textures/bird.bmp")
bird.position.z = -8
bird.position.y = 1.8
bird.position.x = 0
bird.rotation.y = 180
bird.rotation.x = 90
bird.rotation.z = -50
bird.scale.x = 0.1
bird.scale.y = 0.1
bird.scale.z = 0.1
bird.visible = True

dog = Model("models/dog.obj")
dog.AddTexture("textures/dog.bmp")
dog.position.z = -5
dog.position.y = -0.8
dog.position.x = -1.5
dog.rotation.y = 180
dog.rotation.x = 90
dog.rotation.z = 210
dog.scale.x = 0.05
dog.scale.y = 0.05
dog.scale.z = 0.05
dog.visible = True

grass = Model("models/grass.obj")
grass.AddTexture("textures/grass.bmp")
grass.position.z = -7
grass.position.y = -1
grass.position.x = 0
grass.rotation.x = -90
grass.scale.x = 0.02
grass.scale.y = 0.02
grass.scale.z = 0.02
grass.visible = True

wheel = Model("models/wheel.obj")
wheel.AddTexture("textures/wheel.bmp")
wheel.position.z = -8
wheel.position.y = 0.5
wheel.position.x = 0
wheel.rotation.y = 90
wheel.visible = True

penguinPresets = [
    (vertex_shader, fragment_shader),
    (vertex_shader, outline_shader),
    (melt_shader, outline_shader),
    (twist_shader, outline_shader),
    (wave_shader, outline_shader),
    (pulse_shader, outline_shader),
    (shatter_shader, outline_shader)
]

birdPresets = [
    (vertex_shader, fragment_shader),
    (vertex_shader, frozen_shader),
    (melt_shader, frozen_shader),
    (twist_shader, frozen_shader),
    (wave_shader, frozen_shader),
    (pulse_shader, frozen_shader),
    (shatter_shader, frozen_shader)
]

dogPresets = [
    (vertex_shader, fragment_shader),
    (vertex_shader, bubble_shader),
    (twist_shader, bubble_shader),
    (pulse_shader, bubble_shader),
    (wave_shader, bubble_shader),
    (melt_shader, bubble_shader),
    (shatter_shader, bubble_shader)
]

grassPresets = [
    (vertex_shader, fragment_shader),
    (vertex_shader, fire_shader),
    (wave_shader, fire_shader),
    (twist_shader, fire_shader),
    (pulse_shader, fire_shader),
    (melt_shader, fire_shader),
    (shatter_shader, fire_shader)
]

wheelPresets = [
    (vertex_shader, fragment_shader),
    (vertex_shader, glitch_shader),
    (twist_shader, glitch_shader),
    (melt_shader, glitch_shader),
    (pulse_shader, glitch_shader),
    (wave_shader, glitch_shader),
    (shatter_shader, glitch_shader)
]

modelConfigs = [
    ModelShaderConfig(penguin, "Pingüino", penguin.position, penguinPresets),
    ModelShaderConfig(bird, "Pájaro", bird.position, birdPresets),
    ModelShaderConfig(dog, "Perro", dog.position, dogPresets),
    ModelShaderConfig(grass, "Pasto", grass.position, grassPresets),
    ModelShaderConfig(wheel, "Rueda", wheel.position, wheelPresets)
]

focusedModelIndex = 0
camAngle = 0
camElevation = 0
camDistance = 5
camVerticalOffset = 0

currentTarget = modelConfigs[focusedModelIndex].position

isRunning = True

while isRunning:

    deltaTime = clock.tick(60) / 1000
    rend.elapsedTime += deltaTime

    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.MOUSEWHEEL:
            camDistance -= event.y * deltaTime * 50
            camDistance = max(1.0, min(20.0, camDistance))

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:
                focusedModelIndex = (focusedModelIndex + 1) % len(modelConfigs)
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_1:
                focusedModelIndex = 0
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_2:
                focusedModelIndex = 1
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_3:
                focusedModelIndex = 2
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_4:
                focusedModelIndex = 3
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_5:
                focusedModelIndex = 4
                currentTarget = modelConfigs[focusedModelIndex].position
            
            if event.key == pygame.K_h:
                for config in modelConfigs:
                    config.nextPreset()
        
            
            if event.key == pygame.K_r:
                for config in modelConfigs:
                    config.currentPreset = 0
                    config.compileCurrentShader()
            
            if event.key == pygame.K_f:
                rend.ToggleFilledMode()

    if keys[K_UP]:
        camDistance -= 3 * deltaTime
        camDistance = max(1.0, min(20.0, camDistance))

    if keys[K_DOWN]:
        camDistance += 3 * deltaTime
        camDistance = max(1.0, min(20.0, camDistance))

    if keys[K_RIGHT]:
        camAngle += 80 * deltaTime

    if keys[K_LEFT]:
        camAngle -= 80 * deltaTime

    if keys[K_w]:
        camVerticalOffset += 2 * deltaTime

    if keys[K_s]:
        camVerticalOffset -= 2 * deltaTime

    if keys[K_q]:
        camElevation += 50 * deltaTime
        camElevation = max(-89, min(89, camElevation))

    if keys[K_e]:
        camElevation -= 50 * deltaTime
        camElevation = max(-89, min(89, camElevation))

    if keys[K_z]:
        if rend.value > 0.0:
            rend.value -= 1 * deltaTime

    if keys[K_x]:
        if rend.value < 1.0:
            rend.value += 1 * deltaTime

    if pygame.mouse.get_pressed()[0]:
        camAngle += mouseVel[0] * deltaTime * 15
        camElevation += mouseVel[1] * deltaTime * 15
        camElevation = max(-89, min(89, camElevation))

    adjustedTarget = glm.vec3(currentTarget.x, currentTarget.y + camVerticalOffset, currentTarget.z)
    
    rend.camera.Orbit(adjustedTarget, camDistance, camAngle, camElevation)
    rend.camera.LookAt(adjustedTarget)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rend.camera.Update()
    
    if rend.skybox is not None:
        rend.skybox.Render()
    
    for config in modelConfigs:
        if config.model.visible:
            config.useShader(rend.camera, rend.pointLight, rend.ambientLight, rend.elapsedTime, rend.value)
            config.model.Render()

    pygame.display.flip()

pygame.quit()
