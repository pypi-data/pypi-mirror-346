# hyperboost

Подходит как для исследовательских задач, так и для практического использования в реальных проектах.


## ✅ Поддерживаемые методы

| Метод                  | Описание |
|------------------------|----------|
| `BayesianOptimizer`    | Байесовская оптимизация с использованием Gaussian Process |
| `EvolutionaryOptimizer` | Простой генетический алгоритм (GA) |


## 📦 Установка

```bash
pip install hyperoptlib
```

## 🧪 Пример использования

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from hyperboost.space import SearchSpace
from hyperboost.space import Real, Integer, Categorical
from hyperboost.optimizers import BayesianOptimizer
from hyperboost.optimizers import EvolutionaryOptimizer

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

space = SearchSpace({
    "n_estimators": Integer(50, 300),
    "max_depth": Integer(3, 20),
    "criterion": Categorical(["gini", "entropy"]),
})

def objective(params):
    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    return -score  # минимизируем ошибку

# Байесовская оптимизация
bo = BayesianOptimizer(space, objective)
best_bo = bo.optimize(n_iter=30)
print("Bayesian best:", best_bo)

# Эволюционный алгоритм
ea = EvolutionaryOptimizer(space, objective)
best_ea = ea.optimize(population_size=20, generations=10)
print("Evolutionary best:", best_ea)
```

