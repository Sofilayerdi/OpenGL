

vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''



melt_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float value;


void main()
{
    vec3 pos = inPosition;
    
    float meltFactor = max(0.0, pos.y) * value;
    
    pos.y -= meltFactor * 2.0;
    
    float wave = sin(value * 10.0 + pos.x * 5.0) * 0.1;
    pos.x += wave * meltFactor;
    pos.z += sin(value * 8.0 + pos.z * 4.0) * 0.1 * meltFactor;
    
    float spread = meltFactor * 0.3;
    pos.x += normalize(pos).x * spread;
    pos.z += normalize(pos).z * spread;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}

'''

twist_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    float angle = pos.y * value * 3.0 + time * 2.0;
    
    float cosA = cos(angle);
    float sinA = sin(angle);
    
    vec3 twistedPos;
    twistedPos.x = pos.x * cosA - pos.z * sinA;
    twistedPos.y = pos.y;
    twistedPos.z = pos.x * sinA + pos.z * cosA;
    
    vec3 twistedNormal;
    twistedNormal.x = inNormals.x * cosA - inNormals.z * sinA;
    twistedNormal.y = inNormals.y;
    twistedNormal.z = inNormals.x * sinA + inNormals.z * cosA;
    
    fragPosition = modelMatrix * vec4(twistedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(twistedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''

shatter_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

float random(vec3 pos) {
    return fract(sin(dot(pos, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

void main()
{
    vec3 pos = inPosition;
    
    // Calcular dirección de fragmentación basada en posición
    vec3 fragmentDir = normalize(pos + vec3(
        random(pos + vec3(1.0, 0.0, 0.0)),
        random(pos + vec3(0.0, 1.0, 0.0)),
        random(pos + vec3(0.0, 0.0, 1.0))
    ));
    
    // Fragmentación con diferentes velocidades
    float fragmentSpeed = random(pos) * 0.5 + 0.5;
    float shatterAmount = value * fragmentSpeed;
    
    // Movimiento de fragmentos
    pos += fragmentDir * shatterAmount * 2.0;
    
    // Rotación de fragmentos individuales
    float angle = shatterAmount * random(pos) * 10.0 + time;
    float cosA = cos(angle);
    float sinA = sin(angle);
    
    // Rotación en Y
    vec3 rotatedPos;
    rotatedPos.x = pos.x * cosA - pos.z * sinA;
    rotatedPos.y = pos.y;
    rotatedPos.z = pos.x * sinA + pos.z * cosA;
    
    // Caída por gravedad
    rotatedPos.y -= shatterAmount * shatterAmount * 1.5;
    
    // Dispersión adicional con el tiempo
    float timeEffect = sin(time * 2.0 + random(pos) * 6.28) * 0.5 + 0.5;
    rotatedPos += fragmentDir * timeEffect * shatterAmount * 0.3;
    
    fragPosition = modelMatrix * vec4(rotatedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    // Rotar normales también
    vec3 rotatedNormal;
    rotatedNormal.x = inNormals.x * cosA - inNormals.z * sinA;
    rotatedNormal.y = inNormals.y;
    rotatedNormal.z = inNormals.x * sinA + inNormals.z * cosA;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(rotatedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''

wave_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    // Crear ondas en X y Z
    float waveX = sin(pos.y * 5.0 + time * 2.0) * value * 0.3;
    float waveZ = cos(pos.y * 4.0 + time * 2.5) * value * 0.3;
    
    // Ondas circulares desde el centro
    float dist = length(pos.xz);
    float circularWave = sin(dist * 8.0 - time * 3.0) * value * 0.2;
    
    pos.x += waveX;
    pos.z += waveZ;
    pos.y += circularWave;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


pulse_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    // Pulso que se expande desde el centro
    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    pulse = pow(pulse, 2.0);
    
    // Expandir/contraer el modelo
    float scale = 1.0 + pulse * value * 0.5;
    pos *= scale;
    
    // Deformación adicional basada en la distancia del centro
    float dist = length(pos);
    float deform = sin(dist * 5.0 - time * 4.0) * value * 0.1;
    
    vec3 dir = normalize(pos);
    pos += dir * deform;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''
