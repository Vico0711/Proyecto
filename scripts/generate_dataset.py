"""
Script para generar datasets sintéticos COMPLETOS de asignación docente
Versión: 3.1 - CORREGIDO (sin KeyError)
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================
np.random.seed(42)

NUM_DOCENTES = 50

AREAS = [
    'Programación',
    'Base de Datos',
    'Matemáticas',
    'Software',
    'Gestión Computacional',
    'Administración',
    'Computación'
]

# Mapeo de áreas a claves normalizadas (SIN TILDES, SIN ESPACIOS)
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
        'tiene_maestria': 0.07,
        'tiene_doctorado': 0.03,
        'anios_experiencia_docente_total': 0.12,
        'anios_experiencia_industria': 0.18,
        'comp_programacion': 0.23,
        'comp_bases_datos': 0.04,
        'comp_software': 0.14,
        'comp_matematicas': 0.01,
        'comp_gestion_compu': 0.01,
        'comp_administracion': 0.01,
        'comp_computacion': 0.01,
        'total_certificaciones': 0.06,
        'proyectos_desarrollo_reales': 0.09
    },
    'Software': {
        'tiene_maestria': 0.12,
        'tiene_doctorado': 0.05,
        'anios_experiencia_docente_total': 0.10,
        'anios_experiencia_industria': 0.18,
        'comp_software': 0.25,
        'comp_programacion': 0.20,
        'comp_bases_datos': 0.10,
        'comp_matematicas': 0.03,
        'total_certificaciones': 0.05,
        'proyectos_software_reales': 0.13
    },
    'Base de Datos': {
        'tiene_maestria': 0.12,
        'tiene_doctorado': 0.05,
        'anios_experiencia_docente_total': 0.10,
        'anios_experiencia_industria': 0.18,
        'comp_bases_datos': 0.25,
        'comp_programacion': 0.12,
        'comp_software': 0.10,
        'total_certificaciones': 0.08,
        'proyectos_bd_reales': 0.10
    },
    'Matemáticas': {
        'tiene_maestria': 0.15,
        'tiene_doctorado': 0.08,
        'anios_experiencia_docente_total': 0.15,
        'anios_experiencia_industria': 0.08,
        'comp_matematicas': 0.30,
        'comp_programacion': 0.03,
        'proyectos_matematicos_reales': 0.02
    },
    'Gestión Computacional': {
        'tiene_maestria': 0.12,
        'tiene_doctorado': 0.03,
        'anios_experiencia_docente_total': 0.10,
        'anios_experiencia_industria': 0.15,
        'comp_gestion_compu': 0.25,
        'comp_software': 0.10,
        'comp_programacion': 0.08,
        'total_certificaciones': 0.05,
        'proyectos_infraestructura_reales': 0.08
    },
    'Administración': {
        'tiene_maestria': 0.12,
        'tiene_doctorado': 0.03,
        'anios_experiencia_docente_total': 0.10,
        'comp_administracion': 0.25,
        'comp_pedagogica_comunicacion': 0.15,
        'produccion_academica': 0.12,
        'total_certificaciones': 0.05
    },
    'Computación': {
        'tiene_maestria': 0.12,
        'tiene_doctorado': 0.05,
        'anios_experiencia_docente_total': 0.15,
        'comp_computacion': 0.25,
        'comp_tec_herramientas_colaborativas': 0.15,
        'total_certificaciones': 0.05
    }
}

# ============================================
# FUNCIONES AUXILIARES
# ============================================
def generar_competencias_docente(area_principal):
    """
    Genera competencias coherentes según área
    IMPORTANTE: Usa claves SIN TILDES ni espacios problemáticos
    """
    competencias = {}
    
    # Inicializar TODAS las competencias con valores bajos
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        competencias[f'comp_{key_normalizada}'] = round(np.random.uniform(1.0, 2.5), 2)
    
    # Área principal: experto (4-5)
    key_principal = AREA_TO_KEY[area_principal]
    competencias[f'comp_{key_principal}'] = round(np.random.uniform(4.0, 5.0), 2)
    
    # Áreas relacionadas: medio-alto (2.5-4)
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
    """Convierte cantidad de proyectos a score 0-5"""
    if cantidad >= umbral:
        return 5.0
    else:
        return round(min(5.0, (cantidad / umbral) * 5), 2)

def generar_proyectos_por_area(area_principal):
    """Genera proyectos específicos por área"""
    umbrales = {
        'Programación': 10,
        'Software': 5,
        'Base de Datos': 5,
        'Matemáticas': 2,
        'Gestión Computacional': 3,
        'Administración': 3,
        'Computación': 3
    }
    
    proyectos = {}
    
    for area, umbral in umbrales.items():
        if area == area_principal:
            # Área principal: alta probabilidad de superar umbral
            if np.random.rand() > 0.2:
                cantidad = np.random.randint(umbral, umbral + 15)
            else:
                cantidad = np.random.randint(int(umbral * 0.7), umbral)
        else:
            # Otras áreas: baja cantidad
            cantidad = np.random.randint(0, int(umbral * 0.6))
        
        score = calcular_score_proyectos(cantidad, umbral)
        
        # Mapeo correcto de áreas a claves
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
    """Genera certificaciones desglosadas"""
    cert = {
        'cert_programacion': 0,
        'cert_cloud': 0,
        'cert_metodologias_agiles': 0,
        'cert_bases_datos': 0,
        'cert_seguridad': 0,
        'cert_otras': 0
    }
    
    # Área principal: más certificaciones
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
    
    # Otras áreas
    cert['cert_otras'] = np.random.randint(0, 2)
    
    return cert

def generar_score_herramientas(area_principal):
    """Genera scores de herramientas por área"""
    scores = {}
    
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        key = f'score_herramientas_{key_normalizada}'
        
        if area == area_principal:
            # Área principal: score alto
            scores[key] = round(np.random.uniform(3.5, 5.0), 2)
        else:
            # Otras áreas: score bajo-medio
            scores[key] = round(np.random.uniform(0.5, 2.5), 2)
    
    return scores

def generar_score_enfoque(area_principal):
    """Genera scores de enfoque pedagógico (booleano)"""
    scores = {}
    
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        key = f'score_enfoque_{key_normalizada}'
        
        if area == area_principal:
            # Área principal: alta probabilidad de match
            scores[key] = np.random.choice([0, 1], p=[0.1, 0.9])
        else:
            # Otras áreas: baja probabilidad
            scores[key] = np.random.choice([0, 1], p=[0.7, 0.3])
    
    return scores

def normalizar_a_0_1(valor, max_esperado):
    """Normaliza valor a escala 0-1"""
    return min(1.0, valor / max_esperado)

def calcular_idoneidad(docente, area):
    """
    Calcula idoneidad para un área específica
    usando la matriz de ponderaciones
    """
    ponderaciones = PONDERACIONES.get(area, {})
    
    # Normalizar valores
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
        'comp_tec_herramientas_colaborativas': docente.get('comp_tec_herramientas_colaborativas', 3) / 5
    }
    
    score = 0.0
    for variable, peso in ponderaciones.items():
        valor = docente_norm.get(variable, 0)
        score += valor * peso
    
    return round(score * 100, 2)

# ============================================
# GENERAR DOCENTES
# ============================================
print("🔄 Generando dataset de docentes...")

docentes = []
for i in range(1, NUM_DOCENTES + 1):
    area_principal = np.random.choice(AREAS)
    
    # Formación
    tiene_maestria = np.random.choice([0, 1], p=[0.2, 0.8])
    tiene_doctorado = np.random.choice([0, 1], p=[0.85, 0.15])
    
    # Experiencia
    anios_experiencia_docente_total = np.random.randint(3, 20)
    anios_experiencia_industria = np.random.randint(2, 15)
    anios_experiencia_area_software = np.random.randint(1, min(anios_experiencia_industria, 12))
    
    # Competencias técnicas (AHORA CON CLAVES CORRECTAS)
    competencias = generar_competencias_docente(area_principal)
    
    # Proyectos por área
    proyectos = generar_proyectos_por_area(area_principal)
    
    # Certificaciones
    cert = generar_certificaciones(area_principal)
    total_cert = sum(cert.values())
    
    # Herramientas
    herramientas = generar_score_herramientas(area_principal)
    
    # Enfoques
    enfoques = generar_score_enfoque(area_principal)
    
    # Competencias pedagógicas
    comp_ped = {
        'comp_pedagogica_planificacion': np.random.randint(2, 6),
        'comp_pedagogica_evaluacion': np.random.randint(2, 6),
        'comp_pedagogica_innovacion': np.random.randint(1, 5),
        'comp_pedagogica_comunicacion': np.random.randint(3, 6)
    }
    
    # Competencias tecnológicas
    comp_tec = {
        'comp_tec_plataformas_virtuales': np.random.randint(2, 6),
        'comp_tec_herramientas_colaborativas': np.random.randint(3, 6),
        'comp_tec_contenido_digital': np.random.randint(2, 5)
    }
    
    # Evaluación
    promedio_evaluacion_docente = round(np.random.uniform(70, 95), 1)
    numero_evaluaciones = np.random.randint(5, 30)
    
    # Crear registro
    docente = {
        'id_docente': f'DOC_{i:03d}',
        'nombres_completos': f'Docente {i:03d}',
        'cedula': f'09{np.random.randint(10000000, 99999999)}',
        'area_principal': area_principal,
        
        # Formación
        'tiene_maestria': tiene_maestria,
        'tiene_doctorado': tiene_doctorado,
        
        # Experiencia
        'anios_experiencia_docente_total': anios_experiencia_docente_total,
        'anios_experiencia_industria': anios_experiencia_industria,
        'anios_experiencia_area_software': anios_experiencia_area_software,
        
        # Competencias técnicas
        **competencias,
        
        # Proyectos
        **proyectos,
        
        # Certificaciones
        **cert,
        'total_certificaciones': total_cert,
        
        # Herramientas
        **herramientas,
        
        # Enfoques
        **enfoques,
        
        # Competencias pedagógicas
        **comp_ped,
        
        # Competencias tecnológicas
        **comp_tec,
        
        # Evaluación
        'promedio_evaluacion_docente': promedio_evaluacion_docente,
        'numero_evaluaciones': numero_evaluaciones
    }
    
    # Calcular idoneidad por área
    for area in AREAS:
        key_normalizada = AREA_TO_KEY[area]
        docente[f'idoneidad_{key_normalizada}'] = calcular_idoneidad(docente, area)
    
    docentes.append(docente)

df_docentes = pd.DataFrame(docentes)

# ============================================
# MATERIAS
# ============================================
print("🔄 Generando dataset de materias...")

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
    materia = {
        'id_materia': f'MAT_{codigo}',
        'codigo': codigo,
        'nombre': nombre,
        'semestre': semestre,
        'area_conocimiento': area,
        'creditos': np.random.choice([3, 4, 5]),
        'horas_teoria': np.random.randint(32, 48),
        'horas_practica': np.random.randint(16, 32),
        'nivel_complejidad': 'Alto' if semestre >= 7 else ('Medio' if semestre >= 4 else 'Bajo')
    }
    materias.append(materia)

df_materias = pd.DataFrame(materias)

# ============================================
# PERFILES IDEALES
# ============================================
print("🔄 Generando dataset de perfiles ideales...")

perfiles_ideales = []
for area in AREAS:
    key_normalizada = AREA_TO_KEY[area]
    perfil = {
        'id_perfil': f'perfil_{key_normalizada}',
        'area_conocimiento': area,
        **{f'peso_{k}': v for k, v in PONDERACIONES[area].items()}
    }
    perfiles_ideales.append(perfil)

df_perfiles_ideales = pd.DataFrame(perfiles_ideales)

# ============================================
# GUARDAR
# ============================================
print("\n💾 Guardando datasets...")

df_docentes.to_csv('docentes.csv', index=False, sep=',')
df_materias.to_csv('materias.csv', index=False)
df_perfiles_ideales.to_csv('perfiles_ideales.csv', index=False)

print("\n✅ Datasets generados exitosamente:")
print(f"   📄 docentes.csv: {len(df_docentes)} registros con {len(df_docentes.columns)} columnas")
print(f"   📄 materias.csv: {len(df_materias)} registros")
print(f"   📄 perfiles_ideales.csv: {len(df_perfiles_ideales)} registros")

print("\n📊 Columnas de docentes generadas:")
print(list(df_docentes.columns))

print("\n📊 Muestra de idoneidad (primeros 3 docentes):")
print(df_docentes[['id_docente', 'area_principal', 'idoneidad_programacion', 'idoneidad_software', 'idoneidad_matematicas']].head(3))

print("\n🎯 ¡Listo para entrenar el modelo!")