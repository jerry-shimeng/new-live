

echo '初始化python'
sudo apt install python3
sudo apt install python3-pip
pip3 install django
sudo pip3 install pymysql


echo '初始化应用'
python3 manage.py makemigrations movie
python3 manage.py migrate