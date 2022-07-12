https://dev.classmethod.jp/articles/webiopi-raspberry-pi-gpio-operation/

https://dev.classmethod.jp/articles/python-script-in-raspberry-pi/

WebIOPiのダウンロード
```
wget https://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
```
```
tar xvzf WebIOPi-0.7.1.tar.gz
```
```
cd WebIOPi-0.7.1
```
```
wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
```
```
patch -p1 -i webiopi-pi2bplus.patch
```
```
sudo ./setup.sh
```
セットアップ画面が「Do you want to access WebIOPi over Internet ? [y/n]」で止まったら、「n」を入力し、エンターキーを押します。（「y」を入力し、エンターキーを押すと、「Weaved IoT Kit」がインストールされます。）

* WebIOPiサービスをsystemctlで操作できるようにするため設定ファイルをダウンロードします。

```
cd /etc/systemd/system/
```
```
sudo wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi.service
```
/home/kaki/work/webiopi/