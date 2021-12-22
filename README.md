# CARLA2HDF5-v2

## 使い方

### 1. このリポジトリをクローンする

 ```sh
 git clone http://git-docker.tasakilab:5051/git/urasaki/carla2hdf5-v2.git
 ```

### 2. dockerイメージをビルドする

 ```sh
 cd carla2hdf5-v2/docker && ./build-docker.sh
 ```

### 3. dockerからX Window Systemへのアクセスを許可する（dockerの外で）

 ```sh
 xhost +
 ```

### 4. コンテナをそれぞれ別のターミナルで2つ立ち上げる

 ① サーバ用コンテナ
 ```sh
 ./run-carla-server-docker.sh
 ```

 ② carla2hdf5用コンテナ
 ```sh
 ./run-carla2hdf5-docker.sh
 ```

### 5. 実行

 ①のターミナルで
 ```sh
 carla-nodisplay
 ```

 ②のターミナルで
 ```sh
 cd src && python carla2hdf5.py
 ```

### 6. GUI上で    

    a. 左側のInitial Settingsで`Connect`を押しサーバと接続する  
    b. 右側のTask Settingsの`Map`でマップを、`Weather`で天候を選択する  
    c. 右側のTask Settingsの`# Freames`で保存する枚数を、`# NPC *`でNPCの数を選択する  
    d. `Add Task`を押すことで開始される  

### 7. 終了したらX Window Systemへのアクセス許可を取り消す（dockerの外で）

 ```sh
 xhost -
 ```
