# Project_AlphaBot
Client and server(TCP)  which allows you to control the alphabot robot, thanks also to the use of an sqlite database

## API Reference

### Simple Movements

| Name      | Description                        | Video |
| :-------- | :--------------------------------- | :------------------------- |
| `f:time`  | This command allows the AlphaBot to move **forward** for a certain time (based on the **time** value)          | ![gif](./img/fAlphaBot.gif)|
| `b:time`  | This command allows the AlphaBot to move **backwards** for a certain time (based on the **time** value)        | ![gif not present](./img/b.gif)|
| `l:agle`  | This command allows the AlphaBot to rotate to the **left** for a certain angle (based on the **angle** value)  | ![gif not present](./img/l.gif)|
| `r:angle` | This command allows the AlphaBot to rotate to the **right** for a certain angle (based on the **angle** value) | ![gif not present](./img/r.gif)|

### Complex Movements

These movements are stored in a database (**DB_AlphaBot.db**)

| Name        | Description                         | Video|
| :---------- | :---------------------------------- | :-------------------------------- |
| `ZigZag`    | ![ZiZag image](./img/ZigZag.png)    | ![gif not present](./img/ZigZag.gif) |
| `Cerchio`   | ![Cerchio image](./img/Cerchio.png) | ![gif not present](./img/CerchioZag.gif) |
| `Otto`      | ![Otto image](./img/Otto.png)       | ![gif not present](./img/Otto.gif) |
| `Slalom`    | ![Slalom image](./img/Slalom.png)   | ![gif not present](./img/Slalom.gif) |
| `720`       | ![720 image](./img/Cerchio.png)     | ![gif not present](./img/720.gif) |


## Authors

- [@Nicholas-Becchis](https://github.com/Nicholas-Becchis)
- [@GabrieleFerrero](https://github.com/GabrieleFerrero)

  
