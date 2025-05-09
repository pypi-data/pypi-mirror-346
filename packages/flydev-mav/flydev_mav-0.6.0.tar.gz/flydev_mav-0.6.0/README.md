# flydev-mav# 🛸 FlyDev Comandos

**FlyDev Comandos** é uma biblioteca Python em **português brasileiro** que facilita o controle de drones com MAVLink usando a poderosa `pymavlink`. Ideal para iniciantes e desenvolvedores que preferem comandos claros, documentados e em português.

---

## 🚀 Principais Funcionalidades

- 📡 Conexão com o drone via MAVLink
- 🔐 Armar e desarmar motores
- ✈️ Decolar, pousar e mudar modo de voo
- 🕹️ Movimentar o drone (frente, trás, girar)
- 🧠 Todos os comandos com nomes e comentários em português

---

## 📦 Instalação

```bash
pip install flydev-comandos


from flydev_comandos.drone import Drone

# Conecte à porta serial do drone
drone = Drone('/dev/ttyUSB0')

# Armar e decolar
drone.armar()
drone.mudar_modo_voo('GUIDED')
drone.decolar(3)

# Movimentos básicos
drone.ir_para_frente(1.0)
drone.girar_direita(20)

# Pousar e finalizar
drone.pousar()
drone.desarmar()
drone.encerrar()



| Método                 | Descrição                                     |
| ---------------------- | --------------------------------------------- |
| `armar()`              | Arma os motores do drone                      |
| `desarmar()`           | Desarma os motores do drone                   |
| `mudar_modo_voo(modo)` | Altera o modo de voo (`'GUIDED'`, `'LOITER'`) |
| `decolar(altura)`      | Decola até a altura desejada (em metros)      |
| `pousar()`             | Inicia o pouso do drone                       |
| `ir_para_frente()`     | Move o drone para frente                      |
| `ir_para_tras()`       | Move o drone para trás                        |
| `girar_direita()`      | Gira o drone para a direita                   |
| `girar_esquerda()`     | Gira o drone para a esquerda                  |
| `encerrar()`           | Fecha a conexão com o drone                   |
```

## 🛠️ Requisitos
Python 3.6+

pymavlink

Acesso à porta serial do drone (ex: /dev/ttyUSB0)