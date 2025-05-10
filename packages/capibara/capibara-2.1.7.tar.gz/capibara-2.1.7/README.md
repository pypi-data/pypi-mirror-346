# CapibaraGPT-v2 🦫

Modelo de lenguaje avanzado con capacidades de interpretación semiótica y procesamiento de contexto dinámico.

## 🚀 Características Principales

### 1. Módulo Semiótico
- **Interpretación Multi-nivel**: Análisis literal, cultural y simbólico
- **Atención Cruzada**: Integración dinámica de contexto
- **Polisemia Adaptativa**: Pesos dinámicos por tipo de interpretación
- **Métricas Sin Estado**: Compatible con JAX/Flax

### 2. Arquitectura Modular
- **Submodelos Especializados**: Cada módulo con responsabilidad única
- **Router Dinámico**: Selección inteligente de submodelos
- **Meta-loop**: Aprendizaje de patrones de uso

### 3. Procesamiento de Contexto
- **Atención Multi-cabeza**: 4 cabezas de atención
- **Conexiones Residuales**: Mejor flujo de gradientes
- **Dropout Adaptativo**: Regularización por tipo de interpretación

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/CapibaraGPT-v2.git
cd CapibaraGPT-v2

# Instalar dependencias
pip install -r requirements.txt
```

## 📦 Dependencias Principales

```python
jax>=0.4.13
flax>=0.7.4
transformers>=4.30.0
numpy>=1.24.0
pandas>=2.0.0
```

## 🧠 Uso del Módulo Semiótico

```python
from capibara.sub_models.experimental.semio import SemioModule

# Inicialización
semio = SemioModule(
    hidden_size=256,
    dropout_rate=0.1,
    num_heads=4
)

# Forward pass
output = semio(
    x=input_tensor,  # [batch, seq, hidden]
    context=context_tensor,  # [batch, ctx, hidden]
    training=True
)

# Acceso a resultados
interpretations = output["interpretations"]
weights = output["weights"]
semantic = output["semantic_projection"]
metrics = output["metrics"]
```

## 🔍 Características del Módulo Semiótico

### 1. Interpretaciones
- **Literal**: Análisis directo y denotativo
- **Cultural**: Interpretación basada en contexto cultural
- **Simbólica**: Análisis simbólico y connotativo

### 2. Sistema de Pesos
- Proyección semántica para enriquecimiento
- Pesos dinámicos por tipo de interpretación
- Normalización mediante softmax

### 3. Métricas
- Score de polisemia
- Uso de contexto
- Pesos de interpretación

## 🎯 Ejemplos de Uso

### 1. Análisis Semiótico Básico
```python
# Análisis de texto
result = semio.analyze_text("El gato negro cruzó la calle")
print(result["interpretations"])
```

### 2. Integración con Contexto
```python
# Análisis con contexto cultural
result = semio.analyze_with_context(
    text="El gato negro cruzó la calle",
    context="En la cultura egipcia, los gatos negros..."
)
```

## 📊 Métricas y Monitoreo

El módulo registra automáticamente:
- Pesos de polisemia
- Salida de atención
- Pesos de interpretación
- Uso de contexto

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 👥 Autores

- **Anachroni s.coop** - *Desarrollo inicial* - [@gmarko](https://github.com/capibara-team)

## 🙏 Agradecimientos

- Inspirado en la teoría semiótica de Umberto Eco
- Basado en arquitecturas modernas de transformers
- Integración con JAX/Flax para eficiencia computacional 