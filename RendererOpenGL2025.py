import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader 
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/cube_left.png",
				  "skybox/cube_right.png",
				  "skybox/cube_up.png",
				  "skybox/cube_down.png",
				  "skybox/cube_front.png",
				  "skybox/cube_back.png"]

rend.CreateSkybox(skyboxTextures)


faceModel = Model("models/Penguin.obj")
faceModel.AddTexture("textures/Penguin.bmp")
faceModel.position.z = -5
faceModel.visible = False


bird = Model("models/bird.obj")
bird.AddTexture("textures/bird.bmp")
bird.position.z = -5
bird.position.y = 0
bird.position.x = 0
bird.rotation.y = 180
bird.rotation.x = 90
bird.scale.x = 0.17
bird.scale.y = 0.17
bird.scale.z = 0.17
bird.visible = False


dog = Model("models/dog.obj")
dog.AddTexture("textures/dog.bmp")
dog.position.z = -5
dog.position.y = 0
dog.position.x = 0
dog.rotation.y = 180
dog.rotation.x = 90
dog.rotation.z = 180
dog.scale.x = 0.05
dog.scale.y = 0.05
dog.scale.z = 0.05
dog.visible = True

modelIndex = 0

camAngle = 0
camElevation = 0
camDistance = 5

rend.scene.append(faceModel)
rend.scene.append(bird)
rend.scene.append(dog)


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
			camDistance -= event.y * deltaTime * 10
			camDistance = max(1.0, min(20.0, camDistance))

		elif event.type == pygame.KEYDOWN:

			if event.key == pygame.K_TAB:
				modelIndex += 1
				modelIndex %= len(rend.scene)
				for i in range(len(rend.scene)):
					rend.scene[i].visible = i == modelIndex
			
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

			if event.key == pygame.K_1:
				currVertexShader = vertex_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_2:
				currVertexShader = melt_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_3:
				currVertexShader = twist_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_4:
				currVertexShader = explode_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_5:
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_6:
				currFragmentShader = outline_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_7:
				currFragmentShader = frozen_shader
				rend.SetShaders(currVertexShader, currFragmentShader)

			if event.key == pygame.K_8:
				currFragmentShader = bubble_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				


	if keys[K_UP]:
		camDistance -= 2 * deltaTime

	if keys[K_DOWN]:
		camDistance += 2 * deltaTime

	if keys[K_RIGHT]:
		camAngle += 50 * deltaTime

	if keys[K_LEFT]:
		camAngle -= 50 * deltaTime



	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime

	
	if pygame.mouse.get_pressed()[0]:
		camAngle += mouseVel[0] * deltaTime * 10
		camElevation += mouseVel[1] * deltaTime * 10
		camElevation = max(-89, min(89, camElevation))

		

	faceModel.rotation.y += 45 * deltaTime
	bird.rotation.z += 45 * deltaTime
	dog.rotation.z += 45 * deltaTime

	rend.camera.Orbit(faceModel.position, camDistance, camAngle, camElevation)
	rend.camera.LookAt(faceModel.position)


	rend.Render()
	pygame.display.flip()

pygame.quit()