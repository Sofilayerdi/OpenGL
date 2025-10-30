# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''

outline_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    float edge = 1.0 - abs(dot(viewDir, fragNormal));
    edge = pow(edge, 2.0);
    
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    vec4 texColor = texture(tex0, fragTexCoords) * intensity;
    
    float wave1 = sin(fragPosition.y * 8.0 - time * 4.0);
    float wave2 = sin(fragPosition.x * 6.0 + time * 3.0);
    float wave3 = sin(fragPosition.z * 10.0 - time * 5.0);
    
    float waves = (wave1 + wave2 + wave3) * 0.3;
    
    float colorShift = time * 1.5 + edge * 5.0 + waves * 2.0;
    vec3 outlineColor = vec3(
        sin(colorShift) * 0.5 + 0.5,
        sin(colorShift + 2.094) * 0.5 + 0.5,
        sin(colorShift + 4.189) * 0.5 + 0.5
    );
    
    float pump = (sin(time * 3.0) * 0.4 + 0.8) * (1.0 + waves * 0.3);
    
    vec3 finalColor = texColor.rgb;
    
    if (edge > 0.4) {
        finalColor = outlineColor * pump * 2.0;
    } else {
        finalColor = mix(texColor.rgb, outlineColor * pump, edge);
    }
    
    fragColor = vec4(finalColor, 1.0);
}
'''


frozen_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    vec3 iceColor = vec3(0.7, 0.85, 1.0);
    
    float noise1 = random(fragTexCoords * 20.0 + time * 0.1);
    float noise2 = random(fragTexCoords * 50.0);
    float crystals = mix(noise1, noise2, 0.5);
    
    float cracks = sin(fragPosition.x * 30.0) * sin(fragPosition.y * 25.0) * sin(fragPosition.z * 35.0);
    cracks = smoothstep(0.7, 0.9, cracks);
    
    float frost = crystals * 0.5 + 0.3;
    
    vec3 viewDir = normalize(-fragPosition.xyz);
    float fresnel = pow(1.0 - abs(dot(viewDir, fragNormal)), 3.0);
    
    vec3 reflections = mix(vec3(0.5, 0.7, 1.0), vec3(1.0, 1.0, 1.0), fresnel);
    
    vec3 frozen = texColor.rgb * 0.4;  // Oscurecer la textura original
    frozen = mix(frozen, iceColor, 0.5);  // Agregar tono azul
    frozen += reflections * fresnel * 0.8;  // Reflejos brillantes
    frozen += vec3(1.0) * cracks * 0.3;  // Grietas brillantes
    frozen *= frost;  // Textura de escarcha
    
    vec3 reflectDir = reflect(-lightDir, fragNormal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64.0);
    frozen += vec3(1.0) * spec * 0.8;
    
    fragColor = vec4(frozen * (intensity + 0.3), texColor.a);
}
'''

bubble_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

float random(vec3 pos) {
    return fract(sin(dot(pos.xyz, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

void main()
{
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    
    float fresnel = pow(1.0 - abs(dot(viewDir, fragNormal)), 3.0);
    
    vec3 bubbleColor = vec3(0.8, 0.3, 0.9);  // Rosa-púrpura
    
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec3 reflectDir = reflect(-lightDir, fragNormal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 128.0);
    
    vec3 altLightDir = normalize(vec3(1.0, 1.0, 0.5));
    vec3 altReflectDir = reflect(-altLightDir, fragNormal);
    float altSpec = pow(max(dot(viewDir, altReflectDir), 0.0), 64.0);
    
    float iridescence = sin(fresnel * 3.14159 + time * 0.5) * 0.5 + 0.5;
    vec3 iridColor = mix(vec3(0.6, 0.2, 0.8), vec3(0.9, 0.4, 1.0), iridescence);
    
    vec3 sparklePos = vec3(fragTexCoords * 30.0, fragPosition.z * 10.0);
    
    float sparkle1 = random(floor(sparklePos + time * 0.5));
    float sparkle2 = random(floor(sparklePos * 1.5 + time * 0.7));
    float sparkle3 = random(floor(sparklePos * 0.8 + time * 0.3));
    
    float twinkle1 = sin(time * 10.0 + sparkle1 * 50.0) * 0.5 + 0.5;
    float twinkle2 = sin(time * 12.0 + sparkle2 * 60.0) * 0.5 + 0.5;
    float twinkle3 = sin(time * 8.0 + sparkle3 * 40.0) * 0.5 + 0.5;
    
    float sparkleIntensity = 0.0;
    
    if (sparkle1 > 0.90) {
        sparkleIntensity += pow(twinkle1, 3.0) * 3.0;
    }
    if (sparkle2 > 0.92) {
        sparkleIntensity += pow(twinkle2, 3.0) * 2.5;
    }
    if (sparkle3 > 0.88) {
        sparkleIntensity += pow(twinkle3, 3.0) * 2.0;
    }
    
    vec3 sparkleColor = vec3(1.0) * sparkleIntensity * 1.5;
    sparkleColor += vec3(1.0, 0.6, 1.0) * sparkleIntensity * 0.8;
    
    sparkleColor *= (0.5 + fresnel * 1.5);
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    vec3 innerObject = texColor.rgb * 0.4 * (1.0 - fresnel);
    
    vec3 finalColor = bubbleColor * intensity * 0.6;  // Color base
    finalColor = mix(finalColor, iridColor, fresnel * 0.4);  // Iridiscencia en bordes
    finalColor += vec3(1.0) * spec * 2.0;  // Brillos especulares fuertes
    finalColor += vec3(1.0, 0.8, 1.0) * altSpec * 0.8;  // Brillos secundarios
    finalColor += sparkleColor;  // BRILLITOS MÁGICOS
    finalColor += innerObject;  // Objeto dentro
    
    float alpha = 0.3 + fresnel * 0.5;
    
    fragColor = vec4(finalColor, alpha);
}
'''