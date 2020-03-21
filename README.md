# ROSLineFollower
## Описание
Ниже описан простой робот для следования по линии с использованием камеры под управлением мета-операционной системы ROS [[1]](http://robocraft.ru/page/robotics/#ROS). Робот управляется одноплатном компьютером Raspberry Pi 3. Для управления моторами используется плата Arduino Uno и драйвер мотора L298. Для следовании вдоль черной линии используется пропорциональный регулятор [[2]](https://automation-system.ru/main/15-regulyator/type-of-control/90-408-p-pi-pid.html).

## Аппаратная часть 
### Подготовка
Для реализации данного проекта требуются следующие компоненты:
* Одноплатный компьютер Raspberry Pi 3 B+;
![rasp](/images/raspberry.jpg)

* Плата с микроконтроллером Arduino Uno;
![ard](/images/arduino.jpg)

* Веб-камера, подключаемая по USB;
![cam](/images/camera.jpg)

* Электромотор с редуктором и колесом (2 шт);
![mot](/images/motor.jpg)

* Модуль драйвера для 2х электромоторов (L298);
![hb](/images/l298.jpg)

* Карта памяти MicroSD 16 Гб или больше;
* Кабель USB Type A -- USB Type B для соеденения Arduino и Raspberry Pi;
* Батарейный отсек на 4 элемента АА;
* Электрический аккумулятор с возможностью подключения устройств по USB с рабочим напряжением 5 В и током до 2А (подойдут многие современные повербанки)
* Провод для подключения питания для Raspberry (например USB Type A -- Micro USB Type B);
* Провода для макетных плат для подключения Arduino к драйверу моторов;
* Платформа для установки компонентов;
* Провод Ethernet для подключения Raspberry к вашему ПК (необходим Ethernet порт на ПК).

### Сборка 
Сборка электронных компонентов производится по схеме ниже:
![sch](/images/sch.png)
Перед соеденением всех компонентов следует установить все на плтформу. Камера должна быть установлена на высоте 10 - 15 см над уровнем пола, вынесена вперед и направлена почти перпендикулярно полу. Камера должна быть установлена таким образом, чтобы мог быть изменен угол между камерой и полом. Пример установки камеры и других компонентов представлен на рисунках ниже:
![res1](/images/res1.png)
![res2](/images/res2.png)
![res3](/images/res3.png)
![res4](/images/res4.png)

## Программная часть

### Подготовка 
Необходимое программное обеспеченье:
* Операционная система Windows 10 или MacOS 10.14 и выше. Возможно использование ОС Linux;
* ПО для записи образов диска (Win32 Disk Imager/Etcher/аналогичное);
* SSH клиент (При использовании ОС Windows -- Putty, MacOS имеет встроенный SSH клиент);
* Образ ОС Raspbian с установленным ROS и OpenCV. Подробнее об образе написано в [[3]](https://medium.com/@hadabot/ready-to-use-image-raspbian-stretch-ros-opencv-324d6f8dcd96); 
* Утилита nmap;
* Arduino IDE.

### Установка
#### Подготовка Raspberry Pi
Так как процесс установки ROS и OpenCV на чистый образ Raspbian включает множество процедур, в том числе сборку отдельных зависимостей из исходных программных кодов, вместо этого используется готовый образ операционной системы с заранее установленными необходимыми программными пакетами [[3]](https://medium.com/@hadabot/ready-to-use-image-raspbian-stretch-ros-opencv-324d6f8dcd96). Используя Win32 Disk Imager или Etcher  
запишите образ системы на MicroSD карту. Установите карту в Raspberry Pi, подключите питание и подключите raspberry к ПК используя ethernet-кабель. Для подключения по SSH необходимо определить IP-адресс платы, это возможно сделать с использованием утилиты nmap согласно инструкции: [[4]](https://www.raspberrypi.org/documentation/remote-access/ip-address.md). Подключение производится с использованием клинта SSH.
```
Логин: pi
Пароль: rosbots!
```
При использовании клиента в командной строке подключение производится следующей командой (где *raspberry_ip* -- ip-адрес платы):

```
ssh pi@*raspberry_ip*
```
После чего потребуется ввести пароль. При возникновении ошибок с локалью воспользуйтесь следующей инструкцией: [[5]](http://mycyberuniverse.com/ru/error/how-to-fix-setting-locale-failed.html). 

Настройте доступ rasberry к интрнету через ethernet (Windows: [[6]](https://geekylane.com/giving-internet-to-raspberry-pi-using-ethernet-on-from-windows-10/), MacOS [[7]](https://mycyberuniverse.com/mac-os/connect-to-raspberry-pi-from-a-mac-using-ethernet.html)) и точку доступа (без доступа к интернету) [[8]](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md). Включите работу serial порта, запустив команду `sudo raspi-config`, и действуя согласно скриншотам ниже.
![ser1](/images/ser1.png)
![ser2](/images/ser2.png)
![ser3](/images/ser3.png)
![ser4](/images/ser4.png)


Создайте в домашнем каталоге raspberry новую директорию с именем `line_follower` и перейдите в нее.
``` bash
mkdir line_follower
cd line_follower
```
Склонируйте содержимое репозитория в эту директорию и перейдите в новую директорию
``` bash
git clone *repo_address*/ROSLineFollower.git
```

Проверьте, что система ROS запущена, используя команду `roscore`. Если ROS запущен, то появится соответствующее сообщение. Создайте новый пакет ROS c названием line_follower (Подробнее об этом [[9]](http://robocraft.ru/blog/technology/453.html)).
``` bash
roscreate-pkg line_follower std_msgs rospy 
```
Сообщим ROS о существовании нового пакета. Это необходимо делать при каждом новом подключении к Raspberry по SSH, либо добавить соответствующую команду в файл `~/.bashrc`.

```bash
export ROS_PACKAGE_PATH=~/line_follwer:$ROS_PACKAGE_PATH
```
Проверьте, что новый пакет был добавлен. Заппустите команду `rospack profile`. Должны отобразиться все инициализированные в системе пакеты, в том числе `line_follower`. 

Перейдите в новый каталог и скопируйте все нужные файлы из репозитория. Сделайте файлы python исполняемыми.
```bash
cd line_follower
cp -avr ~/ROSLineFollower/nodes ./
cp -avr ~/ROSLineFollower/msg ./
chmod +x nodes/*
```
Измените CMakeLists.txt таким образом, чтобы были сгенерированы кастомные сообщения для ROS. Откройте текстовый редактор nano и раскоментируйте строку `rosbuild_genmsg()`. Подробнее о создании своих сообщений ROS в [[10]](http://robocraft.ru/blog/technology/457.html).

```
nano CMakeLists.txt
```
Запустим сборку пакета.
```
rosmake
```

После этого шага перейдите к настройке Arduino.

#### Подготовка Arduino
Загрузите на ваш ПК содержимое репозитория и запустите Arduino IDE. Подключите Arduino к ПК, откройте папку репозитория arduino и загрузите проект `serial_motors` в Arduino IDE. Настройте подключение Arduino к Arduino IDE (меню *Инструменты* -> *Плата* и *Инструменты* -> *Порт*). Загрузите прошивку на плату. Для проверки работы прошивки подключите моторы к Arduino согласно схеме выше, запустите монитор порта и отправьте команду `256 100 100`. Оба мотора должны будут начать вращаться в одном направлении. После загрузки прошивки подсоедените Arduino к Raspberry с использованием кабеля USB и убедитесь в готовности конструкции (подключение камеры, питания и т.д.)

### Запуск

Отключите Raspberry от ethernet и подключитесь к Wi-f, который раздает плата. Используя ip-адрес, настроенный при создании точки доступа, подключитесь по SSH к плате, создав 3 различных подключения. Проверьте что ваш пакет ROS настроен, запустив команду `rospack profile`. Если пакет не отображается в списке, то запустите команду и проверьте снова.
```bash
export ROS_PACKAGE_PATH=~/line_follwer:$ROS_PACKAGE_PATH
```

Повторите этот пункт во всех сессиях подключения к плате. Запустите следующие команды в 3х различных сессиях подключения (каждая команда в своей сессии).
```bash
rosrun line_follower camera.py
```
```bash
rosrun line_follower control.py
```
```bash
rosrun line_follower motor.py
```

В каждой сессии должны начать появляться переодические сообщения. Моторы робота должны начать вращаться. Если поставить робота на линию, то он долже начать следовать вдоль нее. В случае, если робот следует вдоль линии, но делает это нестабильно, то необходимо менять значение переменной kp в файле nodes/control.py и перезапускать его. Подробнее этот вопрос будет разобран в принципах работы.

#### Демонстрация результатов
Ниже приведен пример запуска робота
![res](/images/output.gif)
## Описание принципа работы

`В разработке`


## Полезные ссылки
1. [Курс обучающих статей о ROS](http://robocraft.ru/page/robotics/#ROS)
2. [Статья посвященная пропорциональному регулятору и не только](https://automation-system.ru/main/15-regulyator/type-of-control/90-408-p-pi-pid.html)
3. [Готовый образ системы для Raspberry Pi](https://medium.com/@hadabot/ready-to-use-image-raspbian-stretch-ros-opencv-324d6f8dcd96)
4. [Инструкция, как узнать ip-адрес Raspberry](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)
5. [Инструкция по настройке локалей](http://mycyberuniverse.com/ru/error/how-to-fix-setting-locale-failed.html)
6. [Инструкция по разадче интернета через кабель в Windows 10](https://geekylane.com/giving-internet-to-raspberry-pi-using-ethernet-on-from-windows-10/)
7. [Инструкция по разадче интернета через кабель в MacOS](https://mycyberuniverse.com/mac-os/connect-to-raspberry-pi-from-a-mac-using-ethernet.html)
8. [Инструкция по настройке точки доступа на raspberry](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
9. [Инструкция, посвященная созданию пакетов ROS](http://robocraft.ru/blog/technology/453.html)
9. [Инструкция, посвященная созданию нестандартных сообщений ROS](http://robocraft.ru/blog/technology/457.html)
