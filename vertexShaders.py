

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


explode_shader = '''
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
    
    vec3 explodeDir = normalize(pos);
    
    float randomOffset = random(pos) * 2.0 - 1.0;
    
    float explosionAmount = value * 3.0;
    
    pos += explodeDir * explosionAmount;
    
    float rotationAngle = explosionAmount * randomOffset * 5.0 + time * 2.0;
    float cosR = cos(rotationAngle);
    float sinR = sin(rotationAngle);
    
    vec3 rotatedPos;
    rotatedPos.x = pos.x * cosR - pos.y * sinR;
    rotatedPos.y = pos.x * sinR + pos.y * cosR;
    rotatedPos.z = pos.z;
    
    float vibration = sin(time * 10.0 + random(pos) * 100.0) * explosionAmount * 0.1;
    rotatedPos += inNormals * vibration;
    
    fragPosition = modelMatrix * vec4(rotatedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''
