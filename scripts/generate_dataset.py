"""
Script para generar dataset sintético de asignaciones docentes
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuración
np.random.seed(42)
NUM_DOCENTES = 30
NUM_ASIGNATURAS = 45
NUM_ASIGNACIONES = 200

# Áreas de conocimiento
AREAS = ['Programación', 'Bases de Datos', 'Matemáticas', 'Software', 
         'Gestión Computacional', 'Administración', 'Computación']

# Generar docentes
docentes = []
for i in range(1, NUM_DOCENTES + 1):
    area_principal = np.random.choice(AREAS)
    
    # Competencias alineadas con el área principal
    comp = {area: np.random.randint(1, 6) for area in AREAS}
    comp[area_principal] = np.random.randint(4, 6)  # Experto en su área
    
    docente = {
        'id_docente': f'DOC_{i:03d}',
        'docente_area': area_principal,
        'tiene_maestria': np.random.choice([0, 1], p=[0.3, 0.7]),
        'tiene_doctorado': np.random.choice([0, 1], p=[0.8, 0.2]),
        'anios_exp_docente': np.random.randint(2, 20),
        'anios_exp_industria': np.random.randint(1, 15),
        'comp_programacion': comp['Programación'],
        'comp_bases_datos': comp['Bases de Datos'],
        'comp_software': comp['Software'],
        'comp_matematicas': comp['Matemáticas'],
        'comp_gestion_compu': comp['Gestión Computacional'],
        'comp_administracion': comp['Administración'],
        'comp_computacion': comp['Computación'],
        'cert_profesionales': np.random.randint(0, 8),
        'proyectos_reales': np.random.randint(0, 15)
    }
    docentes.append(docente)

df_docentes = pd.DataFrame(docentes)

# Generar asignaturas
asignaturas = []
for i in range(1, NUM_ASIGNATURAS + 1):
    area = np.random.choice(AREAS)
    semestre = np.random.randint(1, 11)
    
    asignatura = {
        'id_asignatura': f'MAT_{i:03d}',
        'asignatura_area': area,
        'semestre': semestre,
        'creditos': np.random.choice([3, 4, 5]),
        'teoria': np.random.randint(40, 70),
        'practica': np.random.randint(30, 60),
        'nivel_complejidad': np.random.choice(['Bajo', 'Medio', 'Alto'], p=[0.2, 0.5, 0.3]),
        'requiere_maestria': 1 if semestre >= 7 else np.random.choice([0, 1], p=[0.7, 0.3])
    }
    asignaturas.append(asignatura)

df_asignaturas = pd.DataFrame(asignaturas)

# Generar asignaciones
asignaciones = []
for i in range(1, NUM_ASIGNACIONES + 1):
    docente = df_docentes.sample(1).iloc[0]
    asignatura = df_asignaturas.sample(1).iloc[0]
    
    # Calcular efectividad basada en match
    match_area = 1 if docente['docente_area'] == asignatura['asignatura_area'] else 0
    
    # Calcular score base
    comp_key = f"comp_{asignatura['asignatura_area'].lower().replace(' ', '_')}"
    if comp_key in docente.index:
        comp_relevante = docente[comp_key]
    else:
        comp_relevante = 3
    
    score = (
        match_area * 30 +
        comp_relevante * 10 +
        (docente['anios_exp_docente'] / 20) * 20 +
        (docente['cert_profesionales'] / 8) * 10 +
        (docente['proyectos_reales'] / 15) * 10
    )
    
    # Agregar ruido
    score += np.random.normal(0, 10)
    score = np.clip(score, 0, 100)
    
    # Clasificar efectividad
    if score < 50:
        efectividad = 0  # Bajamente Efectiva
    elif score < 70:
        efectividad = 1  # Medianamente Efectiva
    else:
        efectividad = 2  # Altamente Efectiva
    
    asignacion = {
        'id_asignacion': f'ASG_{i:04d}',
        'id_docente': docente['id_docente'],
        'id_asignatura': asignatura['id_asignatura'],
        'periodo_academico': np.random.choice(['2023-1', '2023-2', '2024-1', '2024-2']),
        'anio': np.random.choice([2023, 2024]),
        'ciclo': np.random.choice([1, 2]),
        'num_estudiantes': np.random.randint(15, 45),
        'tasa_aprobacion': np.random.uniform(0.6, 0.95) if efectividad > 0 else np.random.uniform(0.4, 0.7),
        'promedio_calificaciones': np.random.uniform(6.5, 9.0) if efectividad > 0 else np.random.uniform(5.0, 7.0),
        'evaluacion_docente_periodo': score,
        'efectividad_asignacion': efectividad,
        'match_area': match_area,
        'docente_area': docente['docente_area'],
        'asignatura_area': asignatura['asignatura_area'],
        **{k: docente[k] for k in docente.index if k not in ['id_docente', 'docente_area']},
        **{k: asignatura[k] for k in asignatura.index if k not in ['id_asignatura', 'asignatura_area']}
    }
    asignaciones.append(asignacion)

df_asignaciones = pd.DataFrame(asignaciones)

# Guardar datasets
df_asignaciones.to_csv('data/raw/dataset_asignaciones.csv', index=False)
df_docentes.to_csv('data/raw/docentes.csv', index=False)
df_asignaturas.to_csv('data/raw/asignaturas.csv', index=False)

print("✅ Datasets generados exitosamente:")
print(f"   - Asignaciones: {len(df_asignaciones)} registros")
print(f"   - Docentes: {len(df_docentes)} registros")
print(f"   - Asignaturas: {len(df_asignaturas)} registros")
print(f"\n📊 Distribución de efectividad:")
print(df_asignaciones['efectividad_asignacion'].value_counts().sort_index())