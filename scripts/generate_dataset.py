"""
Script para generar datasets sintéticos COMPLETOS de asignación docente
Versión: 6.0 CORREGIDO - CON NOMBRES REALES Y PREFERENCIAS (SIN ALTERAR SEED)
PARTE 1/2: Configuración, nombres reales, funciones auxiliares
"""

import pandas as pd
import numpy as np
from datetime import datetime
import copy

# ============================================
# CONFIGURACIÓN
# ============================================
np.random.seed(42)

NUM_DOCENTES_BASE = 50
NUM_VARIACIONES_POR_BASE = 3
NUM_PERFILES_NUEVOS = 100
NUM_DOCENTES_TOTAL = NUM_DOCENTES_BASE + (NUM_DOCENTES_BASE * NUM_VARIACIONES_POR_BASE) + NUM_PERFILES_NUEVOS

# ============================================
# NOMBRES REALES DE DOCENTES
# ============================================
NOMBRES_REALES = [
    "ALARCON SALVATIERRA JOSE ABEL",
    "ALONSO ANGUIZACA JOSE LUIS",
    "ALVAREZ SOLIS FRANCISCO XAVIER",
    "AVILES MONROY JORGE ISAAC",
    "BENAVIDES LOPEZ DAVID GONZALO",
    "CALDERON GAVILANES MARLON ADRIAN",
    "CASTRO MARIDUEÑA ADRIANA MARIA",
    "CEDEÑO RODRIGUEZ JUAN CARLOS",
    "COLLANTES FARAH ALEX ROBERTO",
    "CRESPO LEON CHRISTOPHER GABRIEL",
    "CRUZ CHOEZ ANGELICA MARIA",
    "ESPIN RIOFRIO CESAR HUMBERTO",
    "GARCIA ARIAS PEDRO MANUEL",
    "GARCIA ENRIQUEZ MYRIAM CECILIA",
    "GARZON RODAS MAURICIO FERNANDO",
    "GUIJARRO RODRIGUEZ ALFONSO ANIBAL",
    "LEYVA VASQUEZ MAIKEL YELANDI",
    "MACIAS YANQUI OSCAR ALBERTO",
    "MINDA GILCES DIANA ELIZABETH",
    "MOLINA CALDERON MIGUEL ALFONSO",
    "NUÑEZ GAIBOR JEFFERSON ELIAS",
    "PARRALES BRAVO FRANKLIN RICARDO",
    "RAMIREZ VELIZ RICARDO BOLIVAR",
    "RAMOS MOSQUERA BOLIVAR",
    "REYES WAGNIO MANUEL FABRICIO",
    "SANCHEZ PAZMIÑO DIANA PRISCILA",
    "SANTOS DIAZ LILIA BEATRIZ",
    "TEJADA YEPEZ SILVIA LILIANA",
    "VARELA TAPIA ELEANOR ALEXANDRA",
    "YANZA MONTALVAN ANGELA OLIVIA"
]

def generar_nombre_docente(indice):
    """Genera nombre para docente según índice"""
    if indice < len(NOMBRES_REALES):
        return NOMBRES_REALES[indice]
    else:
        # Para docentes adicionales (más de 30), crear variaciones
        base_idx = indice % len(NOMBRES_REALES)
        variacion = (indice // len(NOMBRES_REALES)) + 1
        nombre_base = NOMBRES_REALES[base_idx]
        partes = nombre_base.split()
        if len(partes) >= 3:
            return f"{partes[0]} {partes[1]} {partes[-1]} (V{variacion})"
        return f"{nombre_base} (V{variacion})"

# ============================================
# MATERIAS POR ÁREA (Para preferencias)
# ============================================
MATERIAS_POR_AREA = {
    'Gestión Computacional': [
        'ORGANIZACIÓN Y ARQUITECTURA COMPUTACIONAL',
        'SISTEMAS OPERATIVOS',
        'REDES DE COMPUTADORAS',
        'SEGURIDAD INFORMÁTICA',
        'GESTIÓN DE PROYECTOS DE SOFTWARE',
        'SISTEMAS DE INFORMACIÓN GERENCIAL'
    ],
    'Matemáticas': [
        'CÁLCULO DIFERENCIAL',
        'ESTRUCTURAS DISCRETAS',
        'ÁLGEBRA LINEAL',
        'CÁLCULO INTEGRAL',
        'ESTADÍSTICA I',
        'ESTADÍSTICA II',
        'INVESTIGACIÓN DE OPERACIONES'
    ],
    'Software': [
        'INTRODUCCIÓN A INGENIERÍA DE SOFTWARE',
        'PROCESO DE SOFTWARE',
        'INGENIERÍA DE REQUERIMIENTOS',
        'MODELAMIENTO DE SOFTWARE',
        'DISEÑO Y ARQUITECTURA DE SOFTWARE',
        'INTERACCIÓN HOMBRE - MÁQUINA',
        'CONSTRUCCIÓN DE SOFTWARE',
        'DISEÑO DE EXPERIENCIA DE USUARIO',
        'CALIDAD DEL SOFTWARE',
        'VERIFICACIÓN Y VALIDACIÓN DE SOFTWARE',
        'GESTIÓN DE LA CONFIGURACIÓN DEL SOFTWARE',
        'AUDITORÍA DE SOFTWARE'
    ],
    'Administración': [
        'DEMOCRACIA, CIUDADANÍA Y GLOBALIZACIÓN',
        'LENGUAJE Y COMUNICACIÓN',
        'METODOLOGÍA DE LA INVESTIGACIÓN I',
        'CONTABILIDAD',
        'METODOLOGÍA DE LA INVESTIGACIÓN II',
        'FINANZAS',
        'COMPORTAMIENTO ORGANIZACIONAL',
        'MARCO LEGAL DE LA PROFESIÓN',
        'EMPRENDIMIENTO E INNOVACIÓN'
    ],
    'Programación': [
        'ALGORÍTMOS Y LÓGICA DE PROGRAMACIÓN',
        'PROGRAMACION ORIENTADA A OBJETOS',
        'ESTRUCTURA DE DATOS',
        'PROGRAMACIÓN ORIENTADA A EVENTOS',
        'DESARROLLO DE APLICACIONES WEB',
        'DESARROLLO DE APLICACIONES WEB AVANZADO',
        'DESARROLLO DE APLICACIONES MÓVILES',
        'APLICACIONES DISTRIBUIDAS',
        'INTELIGENCIA ARTIFICIAL'
    ],
    'Base de Datos': [
        'BASE DE DATOS',
        'BASE DE DATOS AVANZADO',
        'INTELIGENCIA DE NEGOCIOS'
    ],
    'Computación': [
        'COMPUTACIÓN I - TIC APLICADAS',
        'COMPUTACIÓN II - TIC PARA LA TOMA DE DECISIONES',
        'COMPUTACIÓN III - TIC PARA PROYECTOS TECNOLÓGICOS'
    ]
}

def generar_preferencias_materias(area_principal, seed_offset):
    """
    ✅ CORREGIDO: Usa seed independiente para no alterar generación de otros features
    Genera lista de 3-5 materias preferidas por el docente.
    """
    # Guardar estado actual del generador
    estado_original = np.random.get_state()
    
    # Usar seed independiente basado en offset
    np.random.seed(42 + seed_offset + 10000)  # +10000 para separar del seed principal
    
    num_materias = np.random.randint(3, 6)
    porcentaje_principal = np.random.uniform(0.6, 0.8)
    num_principal = max(1, int(num_materias * porcentaje_principal))
    num_otras = num_materias - num_principal
    
    preferidas = []
    
    # Materias de su área principal
    if area_principal in MATERIAS_POR_AREA:
        materias_area = MATERIAS_POR_AREA[area_principal]
        if len(materias_area) >= num_principal:
            preferidas.extend(np.random.choice(materias_area, num_principal, replace=False))
        else:
            preferidas.extend(materias_area)
            num_otras += (num_principal - len(materias_area))
    
    # Materias de otras áreas
    if num_otras > 0:
        otras_areas = [a for a in MATERIAS_POR_AREA.keys() if a != area_principal]
        intentos = 0
        while len(preferidas) < num_materias and intentos < 20:
            area_aleatoria = np.random.choice(otras_areas)
            materia_aleatoria = np.random.choice(MATERIAS_POR_AREA[area_aleatoria])
            if materia_aleatoria not in preferidas:
                preferidas.append(materia_aleatoria)
            intentos += 1
    
    resultado = '|'.join(preferidas[:5])
    
    # ✅ RESTAURAR estado original del generador
    np.random.set_state(estado_original)
    
    return resultado

# ============================================
# ÁREAS Y DISTRIBUCIÓN
# ============================================
AREAS = [
    'Programación',
    'Base de Datos',
    'Matemáticas',
    'Software',
    'Gestión Computacional',
    'Administración',
    'Computación'
]

DISTRIBUCION_AREAS = {
    'Software': 75,
    'Gestión Computacional': 60,
    'Programación': 54,
    'Base de Datos': 36,
    'Matemáticas': 33,
    'Computación': 27,
    'Administración': 15
}

AREA_TO_KEY = {
    'Programación': 'programacion',
    'Base de Datos': 'bases_datos',
    'Matemáticas': 'matematicas',
    'Software': 'software',
    'Gestión Computacional': 'gestion_compu',
    'Administración': 'administracion',
    'Computación': 'computacion'
}

# ============================================
# MATRICES DE PONDERACIÓN
# ============================================
PONDERACIONES = {
    'Programación': {
        'tiene_maestria': 0.06, 'tiene_doctorado': 0.02,
        'anios_experiencia_docente_total': 0.10, 'anios_experiencia_industria': 0.15,
        'comp_programacion': 0.20, 'comp_bases_datos': 0.03, 'comp_software': 0.12,
        'total_certificaciones': 0.05, 'proyectos_desarrollo_reales': 0.08,
        'experiencia_total': 0.05, 'ratio_cert_exp': 0.03,
        'veces_impartio_area': 0.08, 'prefiere_area': 0.03
    },
    'Software': {
        'tiene_maestria': 0.10, 'tiene_doctorado': 0.04,
        'anios_experiencia_docente_total': 0.08, 'anios_experiencia_industria': 0.15,
        'comp_software': 0.22, 'comp_programacion': 0.17, 'comp_bases_datos': 0.08,
        'total_certificaciones': 0.04, 'proyectos_software_reales': 0.11,
        'experiencia_total': 0.04, 'veces_impartio_area': 0.07
    },
    'Base de Datos': {
        'tiene_maestria': 0.10, 'tiene_doctorado': 0.04,
        'anios_experiencia_docente_total': 0.08, 'anios_experiencia_industria': 0.15,
        'comp_bases_datos': 0.22, 'comp_programacion': 0.10, 'comp_software': 0.08,
        'total_certificaciones': 0.07, 'proyectos_bd_reales': 0.09,
        'experiencia_total': 0.04, 'veces_impartio_area': 0.07
    },
    'Matemáticas': {
        'tiene_maestria': 0.13, 'tiene_doctorado': 0.07,
        'anios_experiencia_docente_total': 0.13, 'anios_experiencia_industria': 0.07,
        'comp_matematicas': 0.27, 'comp_programacion': 0.03,
        'proyectos_matematicos_reales': 0.02, 'experiencia_total': 0.05,
        'veces_impartio_area': 0.10, 'produccion_academica': 0.08
    },
    'Gestión Computacional': {
        'tiene_maestria': 0.10, 'tiene_doctorado': 0.02,
        'anios_experiencia_docente_total': 0.08, 'anios_experiencia_industria': 0.13,
        'comp_gestion_compu': 0.22, 'comp_software': 0.08, 'comp_programacion': 0.07,
        'total_certificaciones': 0.04, 'proyectos_infraestructura_reales': 0.07,
        'experiencia_total': 0.05, 'veces_impartio_area': 0.09
    },
    'Administración': {
        'tiene_maestria': 0.10, 'tiene_doctorado': 0.02,
        'anios_experiencia_docente_total': 0.08, 'comp_administracion': 0.22,
        'comp_pedagogica_comunicacion': 0.13, 'produccion_academica': 0.10,
        'total_certificaciones': 0.04, 'experiencia_total': 0.04,
        'veces_impartio_area': 0.12
    },
    'Computación': {
        'tiene_maestria': 0.10, 'tiene_doctorado': 0.04,
        'anios_experiencia_docente_total': 0.13, 'comp_computacion': 0.22,
        'comp_tec_herramientas_colaborativas': 0.13, 'total_certificaciones': 0.04,
        'experiencia_total': 0.05, 'veces_impartio_area': 0.11
    }
}

# ============================================
# FUNCIONES AUXILIARES (SIN CAMBIOS)
# ============================================
def generar_competencias_docente(area_principal):
    competencias = {}
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        competencias[f'comp_{key_normalizada}'] = round(np.random.uniform(1.0, 2.5), 2)
    
    key_principal = AREA_TO_KEY[area_principal]
    competencias[f'comp_{key_principal}'] = round(np.random.uniform(4.0, 5.0), 2)
    
    relaciones = {
        'Programación': ['software', 'bases_datos', 'computacion'],
        'Software': ['programacion', 'gestion_compu'],
        'Base de Datos': ['programacion', 'software'],
        'Matemáticas': ['programacion'],
        'Gestión Computacional': ['software', 'computacion'],
        'Administración': ['computacion'],
        'Computación': ['programacion', 'administracion']
    }
    
    if area_principal in relaciones:
        for key_rel in relaciones[area_principal]:
            competencias[f'comp_{key_rel}'] = round(np.random.uniform(2.5, 4.0), 2)
    
    return competencias

def calcular_score_proyectos(cantidad, umbral):
    return 5.0 if cantidad >= umbral else round(min(5.0, (cantidad / umbral) * 5), 2)

def generar_proyectos_por_area(area_principal):
    umbrales = {
        'Programación': 10, 'Software': 5, 'Base de Datos': 5,
        'Matemáticas': 2, 'Gestión Computacional': 3,
        'Administración': 3, 'Computación': 3
    }
    
    proyectos = {}
    for area, umbral in umbrales.items():
        if area == area_principal:
            cantidad = np.random.randint(umbral, umbral + 15) if np.random.rand() > 0.2 else np.random.randint(int(umbral * 0.7), umbral)
        else:
            cantidad = np.random.randint(0, int(umbral * 0.6))
        
        score = calcular_score_proyectos(cantidad, umbral)
        
        if area == 'Programación':
            proyectos['proyectos_desarrollo_reales'] = score
        elif area == 'Software':
            proyectos['proyectos_software_reales'] = score
        elif area == 'Base de Datos':
            proyectos['proyectos_bd_reales'] = score
        elif area == 'Matemáticas':
            proyectos['proyectos_matematicos_reales'] = score
        elif area == 'Gestión Computacional':
            proyectos['proyectos_infraestructura_reales'] = score
        elif area == 'Administración':
            proyectos['produccion_academica'] = score
    
    return proyectos

def generar_certificaciones(area_principal):
    cert = {
        'cert_programacion': 0, 'cert_cloud': 0, 'cert_metodologias_agiles': 0,
        'cert_bases_datos': 0, 'cert_seguridad': 0, 'cert_otras': 0
    }
    
    if area_principal == 'Programación':
        cert['cert_programacion'] = np.random.randint(1, 5)
        cert['cert_cloud'] = np.random.randint(0, 2)
    elif area_principal == 'Software':
        cert['cert_metodologias_agiles'] = np.random.randint(1, 4)
        cert['cert_programacion'] = np.random.randint(0, 3)
    elif area_principal == 'Base de Datos':
        cert['cert_bases_datos'] = np.random.randint(1, 3)
        cert['cert_cloud'] = np.random.randint(0, 2)
    elif area_principal == 'Gestión Computacional':
        cert['cert_seguridad'] = np.random.randint(1, 3)
        cert['cert_cloud'] = np.random.randint(0, 2)
    
    cert['cert_otras'] = np.random.randint(0, 2)
    return cert

def generar_score_herramientas(area_principal):
    scores = {}
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        key = f'score_herramientas_{key_normalizada}'
        scores[key] = round(np.random.uniform(3.5, 5.0), 2) if area == area_principal else round(np.random.uniform(0.5, 2.5), 2)
    return scores

def generar_score_enfoque(area_principal):
    scores = {}
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        key = f'score_enfoque_{key_normalizada}'
        scores[key] = np.random.choice([0, 1], p=[0.1, 0.9]) if area == area_principal else np.random.choice([0, 1], p=[0.7, 0.3])
    return scores

def generar_features_disponibilidad():
    return {
        'carga_actual_creditos': np.random.randint(0, 15),
        'horas_disponibles_semana': np.random.randint(15, 40),
        'puede_horario_manana': np.random.choice([0, 1], p=[0.15, 0.85]),
        'puede_horario_tarde': np.random.choice([0, 1], p=[0.05, 0.95]),
        'puede_horario_noche': np.random.choice([0, 1], p=[0.40, 0.60]),
        'disponible_sabados': np.random.choice([0, 1], p=[0.70, 0.30])
    }

def generar_features_experiencia_especifica(area_principal):
    if np.random.rand() > 0.2:
        veces_impartio = np.random.randint(3, 15)
        anos_desde_ultima = np.random.randint(0, 3)
    else:
        veces_impartio = np.random.randint(0, 3)
        anos_desde_ultima = np.random.randint(3, 10)
    
    return {
        'veces_impartio_area': veces_impartio,
        'anos_desde_ultima_vez': anos_desde_ultima,
        'evaluacion_area_promedio': round(np.random.uniform(75, 95), 1) if veces_impartio > 2 else 0
    }

def generar_features_preferencias(area_principal, area_comparar):
    prefiere = 1 if area_principal == area_comparar else 0
    nivel_interes = round(np.random.uniform(4.0, 5.0), 1) if prefiere else round(np.random.uniform(1.0, 3.5), 1)
    return {'prefiere_area': prefiere, 'nivel_interes_area': nivel_interes}

def generar_features_contexto():
    return {
        'distancia_campus_km': round(np.random.uniform(1, 35), 1),
        'anos_en_institucion': np.random.randint(1, 20),
        'tiene_dedicacion_exclusiva': np.random.choice([0, 1], p=[0.4, 0.6])
    }

def calcular_features_derivados(docente_dict):
    experiencia_total = docente_dict.get('anios_experiencia_docente_total', 0) + docente_dict.get('anios_experiencia_industria', 0)
    total_cert = docente_dict.get('total_certificaciones', 0)
    ratio_cert_exp = round(total_cert / experiencia_total, 2) if experiencia_total > 0 else 0.0
    
    competencias_tecnicas = [
        docente_dict.get('comp_programacion', 0), docente_dict.get('comp_software', 0),
        docente_dict.get('comp_bases_datos', 0), docente_dict.get('comp_matematicas', 0),
        docente_dict.get('comp_gestion_compu', 0), docente_dict.get('comp_computacion', 0)
    ]
    promedio_comp_tecnicas = round(sum(competencias_tecnicas) / len(competencias_tecnicas), 2)
    
    return {
        'experiencia_total': experiencia_total,
        'ratio_cert_exp': ratio_cert_exp,
        'promedio_comp_tecnicas': promedio_comp_tecnicas
    }

def normalizar_a_0_1(valor, max_esperado):
    return min(1.0, valor / max_esperado)

def calcular_idoneidad(docente, area):
    ponderaciones = PONDERACIONES.get(area, {})
    
    docente_norm = {
        'tiene_maestria': docente.get('tiene_maestria', 0),
        'tiene_doctorado': docente.get('tiene_doctorado', 0),
        'anios_experiencia_docente_total': normalizar_a_0_1(docente.get('anios_experiencia_docente_total', 0), 20),
        'anios_experiencia_industria': normalizar_a_0_1(docente.get('anios_experiencia_industria', 0), 20),
        'comp_programacion': docente.get('comp_programacion', 0) / 5,
        'comp_bases_datos': docente.get('comp_bases_datos', 0) / 5,
        'comp_software': docente.get('comp_software', 0) / 5,
        'comp_matematicas': docente.get('comp_matematicas', 0) / 5,
        'comp_gestion_compu': docente.get('comp_gestion_compu', 0) / 5,
        'comp_administracion': docente.get('comp_administracion', 0) / 5,
        'comp_computacion': docente.get('comp_computacion', 0) / 5,
        'total_certificaciones': normalizar_a_0_1(docente.get('total_certificaciones', 0), 15),
        'proyectos_desarrollo_reales': docente.get('proyectos_desarrollo_reales', 0) / 5,
        'proyectos_software_reales': docente.get('proyectos_software_reales', 0) / 5,
        'proyectos_bd_reales': docente.get('proyectos_bd_reales', 0) / 5,
        'proyectos_matematicos_reales': docente.get('proyectos_matematicos_reales', 0) / 5,
        'proyectos_infraestructura_reales': docente.get('proyectos_infraestructura_reales', 0) / 5,
        'produccion_academica': docente.get('produccion_academica', 0) / 5,
        'comp_pedagogica_comunicacion': docente.get('comp_pedagogica_comunicacion', 3) / 5,
        'comp_tec_herramientas_colaborativas': docente.get('comp_tec_herramientas_colaborativas', 3) / 5,
        'experiencia_total': normalizar_a_0_1(docente.get('experiencia_total', 0), 35),
        'ratio_cert_exp': normalizar_a_0_1(docente.get('ratio_cert_exp', 0), 1.5),
        'veces_impartio_area': normalizar_a_0_1(docente.get('veces_impartio_area', 0), 15),
        'prefiere_area': docente.get('prefiere_area', 0)
    }
    
    score = sum(docente_norm.get(variable, 0) * peso for variable, peso in ponderaciones.items())
    return round(score * 100, 2)

print("="*70)
print("🚀 GENERADOR v6.0 CORREGIDO - NOMBRES + PREFERENCIAS (SEED PROTEGIDO)")
print("="*70)
print(f"\n📊 Configuración:")
print(f"   - Docentes base: {NUM_DOCENTES_BASE}")
print(f"   - Variaciones: {NUM_VARIACIONES_POR_BASE} × {NUM_DOCENTES_BASE}")
print(f"   - Perfiles nuevos: {NUM_PERFILES_NUEVOS}")
print(f"   - TOTAL: {NUM_DOCENTES_TOTAL}")
print(f"\n✅ {len(NOMBRES_REALES)} nombres reales cargados")
print(f"✅ Sistema de preferencias con SEED INDEPENDIENTE activado")
print("\n" + "="*70)

# ============================================
# FUNCIÓN PRINCIPAL CORREGIDA
# ============================================
def generar_docente_completo(id_num, area_principal, perfil_tipo='normal'):
    """
    ✅ CORREGIDO: Genera docente con preferencias AL FINAL sin alterar seed principal
    """
    
    # Formación según perfil
    if perfil_tipo == 'experto_senior':
        tiene_maestria = 1
        tiene_doctorado = np.random.choice([0, 1], p=[0.3, 0.7])
        anios_experiencia_docente_total = np.random.randint(8, 15)
        anios_experiencia_industria = np.random.randint(12, 20)
    elif perfil_tipo == 'academico_puro':
        tiene_maestria = 1
        tiene_doctorado = np.random.choice([0, 1], p=[0.2, 0.8])
        anios_experiencia_docente_total = np.random.randint(10, 20)
        anios_experiencia_industria = np.random.randint(0, 3)
    elif perfil_tipo == 'junior':
        tiene_maestria = np.random.choice([0, 1], p=[0.3, 0.7])
        tiene_doctorado = 0
        anios_experiencia_docente_total = np.random.randint(3, 7)
        anios_experiencia_industria = np.random.randint(2, 8)
    elif perfil_tipo == 'generalista':
        tiene_maestria = np.random.choice([0, 1], p=[0.2, 0.8])
        tiene_doctorado = np.random.choice([0, 1], p=[0.85, 0.15])
        anios_experiencia_docente_total = np.random.randint(8, 12)
        anios_experiencia_industria = np.random.randint(8, 12)
    else:  # normal
        tiene_maestria = np.random.choice([0, 1], p=[0.2, 0.8])
        tiene_doctorado = np.random.choice([0, 1], p=[0.85, 0.15])
        anios_experiencia_docente_total = np.random.randint(3, 20)
        anios_experiencia_industria = np.random.randint(2, 15)
    
    # FIX: Evitar error cuando experiencia en industria es muy baja
    if anios_experiencia_industria > 1:
        anios_experiencia_area_software = np.random.randint(0, min(anios_experiencia_industria + 1, 13))
    else:
        anios_experiencia_area_software = 0
    
    competencias = generar_competencias_docente(area_principal)
    proyectos = generar_proyectos_por_area(area_principal)
    cert = generar_certificaciones(area_principal)
    total_cert = sum(cert.values())
    
    # Crear docente SIN preferencias primero
    docente = {
        'id_docente': f'DOC_{id_num:03d}',
        'nombres_completos': generar_nombre_docente(id_num - 1),
        'cedula': f'09{np.random.randint(10000000, 99999999)}',
        'area_principal': area_principal,
        'tiene_maestria': tiene_maestria,
        'tiene_doctorado': tiene_doctorado,
        'anios_experiencia_docente_total': anios_experiencia_docente_total,
        'anios_experiencia_industria': anios_experiencia_industria,
        'anios_experiencia_area_software': anios_experiencia_area_software,
        **competencias,
        **proyectos,
        **cert,
        'total_certificaciones': total_cert,
        **generar_score_herramientas(area_principal),
        **generar_score_enfoque(area_principal),
        'comp_pedagogica_planificacion': np.random.randint(2, 6),
        'comp_pedagogica_evaluacion': np.random.randint(2, 6),
        'comp_pedagogica_innovacion': np.random.randint(1, 5),
        'comp_pedagogica_comunicacion': np.random.randint(3, 6),
        'comp_tec_plataformas_virtuales': np.random.randint(2, 6),
        'comp_tec_herramientas_colaborativas': np.random.randint(3, 6),
        'comp_tec_contenido_digital': np.random.randint(2, 5),
        'promedio_evaluacion_docente': round(np.random.uniform(70, 95), 1),
        'numero_evaluaciones': np.random.randint(5, 30),
        **generar_features_disponibilidad(),
        **generar_features_experiencia_especifica(area_principal),
        **generar_features_contexto()
    }
    
    docente.update(calcular_features_derivados(docente))
    docente['perfil_tipo'] = perfil_tipo
    
    # ✅ AGREGAR PREFERENCIAS AL FINAL con seed independiente
    docente['materias_preferidas'] = generar_preferencias_materias(area_principal, id_num)
    
    return docente

# ============================================
# PASO 1: GENERAR DOCENTES BASE
# ============================================
print("\n🔄 PASO 1/4: Generando docentes BASE...")
docentes_base = [generar_docente_completo(i, np.random.choice(AREAS), 'normal') for i in range(1, NUM_DOCENTES_BASE + 1)]
print(f"✅ {len(docentes_base)} docentes base generados")

# ============================================
# PASO 2: GENERAR VARIACIONES
# ============================================
print("\n🔄 PASO 2/4: Generando VARIACIONES...")

def crear_variacion_docente(docente_base, id_nuevo, tipo_variacion=1):
    """Crea variación de un docente base"""
    docente_var = copy.deepcopy(docente_base)
    docente_var['id_docente'] = f'DOC_{id_nuevo:03d}'
    docente_var['nombres_completos'] = generar_nombre_docente(id_nuevo - 1)
    docente_var['cedula'] = f'09{np.random.randint(10000000, 99999999)}'
    
    if tipo_variacion == 1:  # Variación leve
        docente_var['anios_experiencia_docente_total'] = max(3, docente_base['anios_experiencia_docente_total'] + np.random.randint(-2, 3))
        docente_var['anios_experiencia_industria'] = max(2, docente_base['anios_experiencia_industria'] + np.random.randint(-2, 3))
        
        for key in docente_var.keys():
            if key.startswith('comp_') and isinstance(docente_var[key], float):
                nuevo_valor = docente_var[key] + round(np.random.uniform(-0.3, 0.3), 2)
                docente_var[key] = round(max(1.0, min(5.0, nuevo_valor)), 2)
        
        docente_var['perfil_tipo'] = 'variacion_leve'
        
    elif tipo_variacion == 2:  # Variación moderada
        docente_var['anios_experiencia_docente_total'] = max(3, docente_base['anios_experiencia_docente_total'] + np.random.randint(-5, 6))
        docente_var['anios_experiencia_industria'] = max(2, docente_base['anios_experiencia_industria'] + np.random.randint(-5, 6))
        
        for key in docente_var.keys():
            if key.startswith('comp_') and isinstance(docente_var[key], float):
                nuevo_valor = docente_var[key] + round(np.random.uniform(-0.5, 0.5), 2)
                docente_var[key] = round(max(1.0, min(5.0, nuevo_valor)), 2)
        
        for key in ['cert_programacion', 'cert_cloud', 'cert_metodologias_agiles', 
                    'cert_bases_datos', 'cert_seguridad', 'cert_otras']:
            if key in docente_var:
                docente_var[key] = max(0, docente_var[key] + np.random.choice([-1, 0, 1]))
        
        docente_var['total_certificaciones'] = sum([
            docente_var.get('cert_programacion', 0),
            docente_var.get('cert_cloud', 0),
            docente_var.get('cert_metodologias_agiles', 0),
            docente_var.get('cert_bases_datos', 0),
            docente_var.get('cert_seguridad', 0),
            docente_var.get('cert_otras', 0)
        ])
        
        docente_var['perfil_tipo'] = 'variacion_moderada'
        
    elif tipo_variacion == 3:  # Variación formación
        if docente_base['tiene_maestria'] == 0:
            docente_var['tiene_maestria'] = 1
            docente_var['comp_pedagogica_planificacion'] = min(5, docente_var['comp_pedagogica_planificacion'] + 1)
            docente_var['comp_pedagogica_evaluacion'] = min(5, docente_var['comp_pedagogica_evaluacion'] + 1)
        else:
            if np.random.rand() < 0.3:
                docente_var['tiene_maestria'] = 0
        
        docente_var['anios_experiencia_docente_total'] = max(3, docente_base['anios_experiencia_docente_total'] + np.random.randint(-3, 4))
        docente_var['anios_experiencia_industria'] = max(2, docente_base['anios_experiencia_industria'] + np.random.randint(-3, 4))
        
        docente_var['perfil_tipo'] = 'variacion_formacion'
    
    # ✅ Regenerar preferencias AL FINAL con seed independiente
    docente_var['materias_preferidas'] = generar_preferencias_materias(docente_var['area_principal'], id_nuevo)
    
    docente_var.update(calcular_features_derivados(docente_var))
    docente_var.update(generar_features_disponibilidad())
    docente_var['distancia_campus_km'] = round(np.random.uniform(1, 35), 1)
    docente_var['anos_en_institucion'] = np.random.randint(1, 20)
    
    return docente_var

variaciones = []
id_actual = NUM_DOCENTES_BASE + 1

for docente_base in docentes_base:
    for tipo in [1, 2, 3]:
        variacion = crear_variacion_docente(docente_base, id_actual, tipo_variacion=tipo)
        variaciones.append(variacion)
        id_actual += 1

print(f"✅ {len(variaciones)} variaciones generadas")

# ============================================
# PASO 3: GENERAR PERFILES NUEVOS
# ============================================
print("\n🔄 PASO 3/4: Generando perfiles NUEVOS...")

docentes_actuales = docentes_base + variaciones
contador_actual = {area: sum(1 for d in docentes_actuales if d['area_principal'] == area) for area in AREAS}

perfiles_por_area = {}
for area in AREAS:
    faltante = max(0, DISTRIBUCION_AREAS[area] - contador_actual[area])
    perfiles_por_area[area] = faltante

total_perfiles_calculado = sum(perfiles_por_area.values())
if total_perfiles_calculado < NUM_PERFILES_NUEVOS:
    diferencia = NUM_PERFILES_NUEVOS - total_perfiles_calculado
    for i in range(diferencia):
        area = list(DISTRIBUCION_AREAS.keys())[i % len(DISTRIBUCION_AREAS)]
        perfiles_por_area[area] += 1
elif total_perfiles_calculado > NUM_PERFILES_NUEVOS:
    diferencia = total_perfiles_calculado - NUM_PERFILES_NUEVOS
    areas_invertidas = list(reversed(list(DISTRIBUCION_AREAS.keys())))
    for i in range(diferencia):
        area = areas_invertidas[i % len(areas_invertidas)]
        if perfiles_por_area[area] > 0:
            perfiles_por_area[area] -= 1

perfiles_nuevos = []
tipos_perfil = ['experto_senior', 'academico_puro', 'junior', 'generalista']

for area in AREAS:
    cantidad = perfiles_por_area[area]
    for i in range(cantidad):
        tipo_perfil = tipos_perfil[i % len(tipos_perfil)]
        docente = generar_docente_completo(id_actual, area, perfil_tipo=tipo_perfil)
        perfiles_nuevos.append(docente)
        id_actual += 1

print(f"✅ {len(perfiles_nuevos)} perfiles nuevos generados")

# ============================================
# COMBINAR TODOS
# ============================================
print("\n🔄 Combinando todos los docentes...")
todos_docentes = docentes_base + variaciones + perfiles_nuevos
print(f"✅ Total: {len(todos_docentes)} docentes")

contador_final = {area: sum(1 for d in todos_docentes if d['area_principal'] == area) for area in AREAS}
print(f"\n📊 Distribución final por área:")
for area in sorted(contador_final.keys(), key=lambda x: contador_final[x], reverse=True):
    print(f"   - {area}: {contador_final[area]}")

# ============================================
# PASO 4: CALCULAR IDONEIDAD
# ============================================
print("\n🔄 PASO 4/4: Calculando idoneidad por área...")

for idx, docente in enumerate(todos_docentes):
    if (idx + 1) % 50 == 0:
        print(f"   Procesando {idx + 1}/{len(todos_docentes)}...")
    
    area_principal = docente['area_principal']
    
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        preferencias = generar_features_preferencias(area_principal, area)
        
        docente_temp = docente.copy()
        docente_temp['prefiere_area'] = preferencias['prefiere_area']
        docente_temp['veces_impartio_area'] = docente['veces_impartio_area'] if area == area_principal else np.random.randint(0, 3)
        
        docente[f'idoneidad_{key_normalizada}'] = calcular_idoneidad(docente_temp, area)
        docente[f'prefiere_{key_normalizada}'] = preferencias['prefiere_area']
        docente[f'nivel_interes_{key_normalizada}'] = preferencias['nivel_interes_area']

df_docentes = pd.DataFrame(todos_docentes)
print(f"\n✅ Idoneidad calculada para {len(todos_docentes)} docentes")

# ============================================
# GENERAR MATERIAS
# ============================================
print("\n🔄 Generando materias...")

materias_carrera = [
    ('216', 'ORGANIZACIÓN Y ARQUITECTURA COMPUTACIONAL', 2, 'Gestión Computacional'),
    ('315', 'SISTEMAS OPERATIVOS', 3, 'Gestión Computacional'),
    ('414', 'REDES DE COMPUTADORAS', 4, 'Gestión Computacional'),
    ('814', 'SEGURIDAD INFORMÁTICA', 8, 'Gestión Computacional'),
    ('993', 'GESTIÓN DE PROYECTOS DE SOFTWARE', 10, 'Gestión Computacional'),
    ('994', 'SISTEMAS DE INFORMACIÓN GERENCIAL', 10, 'Gestión Computacional'),
    ('112', 'INTRODUCCIÓN A INGENIERÍA DE SOFTWARE', 1, 'Software'),
    ('311', 'PROCESO DE SOFTWARE', 3, 'Software'),
    ('314', 'INGENIERÍA DE REQUERIMIENTOS', 3, 'Software'),
    ('412', 'MODELAMIENTO DE SOFTWARE', 4, 'Software'),
    ('511', 'DISEÑO Y ARQUITECTURA DE SOFTWARE', 5, 'Software'),
    ('514', 'INTERACCIÓN HOMBRE - MÁQUINA', 5, 'Software'),
    ('611', 'CONSTRUCCIÓN DE SOFTWARE', 6, 'Software'),
    ('614', 'DISEÑO DE EXPERIENCIA DE USUARIO', 6, 'Software'),
    ('711', 'CALIDAD DEL SOFTWARE', 7, 'Software'),
    ('811', 'VERIFICACIÓN Y VALIDACIÓN DE SOFTWARE', 8, 'Software'),
    ('911', 'GESTIÓN DE LA CONFIGURACIÓN DEL SOFTWARE', 9, 'Software'),
    ('991', 'AUDITORÍA DE SOFTWARE', 10, 'Software'),
    ('116', 'ALGORÍTMOS Y LÓGICA DE PROGRAMACIÓN', 1, 'Programación'),
    ('212', 'PROGRAMACION ORIENTADA A OBJETOS', 2, 'Programación'),
    ('313', 'ESTRUCTURA DE DATOS', 3, 'Programación'),
    ('515', 'PROGRAMACIÓN ORIENTADA A EVENTOS', 5, 'Programación'),
    ('613', 'DESARROLLO DE APLICACIONES WEB', 6, 'Programación'),
    ('714', 'DESARROLLO DE APLICACIONES WEB AVANZADO', 7, 'Programación'),
    ('813', 'DESARROLLO DE APLICACIONES MÓVILES', 8, 'Programación'),
    ('914', 'APLICACIONES DISTRIBUIDAS', 9, 'Programación'),
    ('915', 'INTELIGENCIA ARTIFICIAL', 9, 'Programación'),
    ('415', 'BASE DE DATOS', 4, 'Base de Datos'),
    ('615', 'BASE DE DATOS AVANZADO', 6, 'Base de Datos'),
    ('715', 'INTELIGENCIA DE NEGOCIOS', 7, 'Base de Datos'),
    ('111', 'CÁLCULO DIFERENCIAL', 1, 'Matemáticas'),
    ('115', 'ESTRUCTURAS DISCRETAS', 1, 'Matemáticas'),
    ('215', 'ÁLGEBRA LINEAL', 2, 'Matemáticas'),
    ('211', 'CÁLCULO INTEGRAL', 2, 'Matemáticas'),
    ('312', 'ESTADÍSTICA I', 3, 'Matemáticas'),
    ('413', 'ESTADÍSTICA II', 4, 'Matemáticas'),
    ('411', 'INVESTIGACIÓN DE OPERACIONES', 4, 'Matemáticas'),
    ('113', 'DEMOCRACIA, CIUDADANÍA Y GLOBALIZACIÓN', 1, 'Administración'),
    ('114', 'LENGUAJE Y COMUNICACIÓN', 1, 'Administración'),
    ('213', 'METODOLOGÍA DE LA INVESTIGACIÓN I', 2, 'Administración'),
    ('214', 'CONTABILIDAD', 2, 'Administración'),
    ('512', 'METODOLOGÍA DE LA INVESTIGACIÓN II', 5, 'Administración'),
    ('513', 'FINANZAS', 5, 'Administración'),
    ('612', 'COMPORTAMIENTO ORGANIZACIONAL', 6, 'Administración'),
    ('713', 'MARCO LEGAL DE LA PROFESIÓN', 7, 'Administración'),
    ('815', 'EMPRENDIMIENTO E INNOVACIÓN', 8, 'Administración'),
    ('066', 'COMPUTACIÓN I - TIC APLICADAS', 1, 'Computación'),
    ('067', 'COMPUTACIÓN II - TIC PARA LA TOMA DE DECISIONES', 2, 'Computación'),
    ('068', 'COMPUTACIÓN III - TIC PARA PROYECTOS TECNOLÓGICOS', 3, 'Computación')
]

materias = []
for codigo, nombre, semestre, area in materias_carrera:
    horas_teoria = np.random.randint(32, 48)
    horas_practica = np.random.randint(16, 32)
    
    materia = {
        'id_materia': f'MAT_{codigo}',
        'codigo': codigo,
        'nombre': nombre,
        'semestre': semestre,
        'area_conocimiento': area,
        'creditos': np.random.choice([3, 4, 5]),
        'horas_teoria': horas_teoria,
        'horas_practica': horas_practica,
        'nivel_complejidad': 'Alto' if semestre >= 7 else ('Medio' if semestre >= 4 else 'Bajo'),
        'ratio_teoria_practica': round(horas_teoria / (horas_practica + 1), 2),
        'es_materia_core': 1 if semestre <= 5 else 0,
        'requiere_laboratorio': 1 if horas_practica >= 20 else 0,
        'tamanio_clase_promedio': np.random.randint(25, 45),
        'requiere_software_especializado': np.random.choice([0, 1], p=[0.6, 0.4]),
        'es_materia_practica': 1 if horas_practica > horas_teoria else 0,
        'nivel_complejidad_num': 2 if semestre >= 7 else (1 if semestre >= 4 else 0)
    }
    materias.append(materia)

df_materias = pd.DataFrame(materias)
print(f"✅ {len(df_materias)} materias generadas")

# ============================================
# PERFILES IDEALES
# ============================================
print("\n🔄 Generando perfiles ideales...")

perfiles_ideales = []
for area in AREAS:
    key_normalizada = AREA_TO_KEY[area]
    perfil = {'id_perfil': f'perfil_{key_normalizada}', 'area_conocimiento': area}
    for variable, peso in PONDERACIONES[area].items():
        perfil[f'peso_{variable}'] = peso
    perfiles_ideales.append(perfil)

df_perfiles_ideales = pd.DataFrame(perfiles_ideales)
print(f"✅ {len(df_perfiles_ideales)} perfiles ideales generados")

# ============================================
# GUARDAR DATASETS
# ============================================
print("\n💾 Guardando datasets...")

df_docentes.to_csv('docentes_v3.csv', index=False, encoding='utf-8')
df_materias.to_csv('materias.csv', index=False, encoding='utf-8')
df_perfiles_ideales.to_csv('perfiles_ideales.csv', index=False, encoding='utf-8')

print("\n" + "="*70)
print("✅ DATASETS v3 GENERADOS EXITOSAMENTE (SEED CORREGIDO)")
print("="*70)

print(f"\n📄 docentes_v3.csv:")
print(f"   - {len(df_docentes)} docentes")
print(f"   - {len(df_docentes.columns)} columnas")
print(f"   - ✅ Nombres reales incluidos")
print(f"   - ✅ Preferencias con SEED INDEPENDIENTE")

print(f"\n📊 Muestra de nombres:")
print(df_docentes[['id_docente', 'nombres_completos', 'area_principal']].head(5).to_string(index=False))

print(f"\n📊 Muestra de preferencias:")
for idx in range(3):
    doc = df_docentes.iloc[idx]
    prefs = doc['materias_preferidas'].split('|') if pd.notna(doc['materias_preferidas']) else []
    print(f"\n{doc['nombres_completos']} ({doc['area_principal']}):")
    for i, pref in enumerate(prefs, 1):
        print(f"   {i}. {pref}")

# Verificación de compatibilidad con v2
print("\n" + "="*70)
print("🔍 VERIFICACIÓN DE COMPATIBILIDAD CON v2")
print("="*70)
print(f"\n📊 Estadísticas clave:")
print(f"   - Idoneidad promedio general: {df_docentes[[col for col in df_docentes.columns if col.startswith('idoneidad_')]].mean().mean():.2f}%")
print(f"   - Experiencia total promedio: {df_docentes['experiencia_total'].mean():.1f} años")
print(f"   - Competencias técnicas promedio: {df_docentes['promedio_comp_tecnicas'].mean():.2f}/5")
print(f"   - Con maestría: {df_docentes['tiene_maestria'].sum()} ({df_docentes['tiene_maestria'].sum()/len(df_docentes)*100:.1f}%)")
print(f"   - Con doctorado: {df_docentes['tiene_doctorado'].sum()} ({df_docentes['tiene_doctorado'].sum()/len(df_docentes)*100:.1f}%)")

print("\n" + "="*70)
print("🎯 ARCHIVOS LISTOS PARA NOTEBOOK v3")
print("="*70)
print("\n✅ Las preferencias NO alteran la generación de otros features")
print("✅ Los datos deberían ser compatibles con resultados de v2")
print("✅ Ahora puedes ejecutar el notebook v3 y comparar métricas")
print("="*70)