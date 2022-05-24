from selenium import webdriver
import time
import argparse
import os
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import requests
import toml
from loguru import logger

cfg = toml.load('config.toml')
logger.add("./log/sim_connect.log", rotation="10 MB", level="INFO")

def perform_login(username, passwd):
    # sudo apt install Xvfb
    # pip install pyvirtualdisplay

    driver = webdriver.Chrome(executable_path=cfg['os']['wd_bin'])
    driver.get(cfg['url']['net_url'])
    time.sleep(1)
    if len(driver.find_elements_by_class_name("disconnect")) == 1:
        logger.warning('online now')
        return
    try:
        input_username = driver.find_element_by_id("username")
        input_passwd = driver.find_element_by_id("password")
    except:
        input_username = driver.find_element_by_id("uname")
        input_passwd = driver.find_element_by_id("pass")
    input_username.send_keys(username)
    input_passwd.send_keys(passwd)
    submit = driver.find_element_by_name("connect")
    submit.click()


def login_timer(username, passwd, timer, notify=True):
    mail_cfg = cfg['mail']
    receivers = mail_cfg['receivers']
    host = mail_cfg['host']
    port = mail_cfg['port']
    max_retry = cfg['connect']['max_retry']
    retry_sleep = cfg['connect']['retry_sleep']
    run_times = 0
    while True:
        connected = False
        retry = 0
        while retry < max_retry:
            try:
                perform_login(username=username, passwd=passwd)
                connected = True
                logger.info("connected login! user is {}", username)
                break
            except:
                logger.error("connecting failed, retry {}...", retry)
                retry += 1
                time.sleep(retry_sleep)

        try:
            ip_text = requests.get(cfg['url']['ip_url'], timeout=1).text.strip()
        except:
            os.system("{} > {}".format(cfg['os']['ip_cmd'], cfg['os']['tmp_file']))
            time.sleep(1)
            with open(cfg['os']['tmp_file'], "r",
                    encoding=cfg['os']['encode']) as f:
                ip_text = f.read()

        sended = False
        retry = 0
        while notify and retry < max_retry:
            try:
                email_addr = '{}@{}'.format(username, host)
                message = MIMEText('当前IP信息如下\n{}'.format(ip_text), 'plain',
                                   'utf-8')
                message['From'] = Header("{} <{}>".format(
                    mail_cfg['from_name'], email_addr), 'utf-8') 
                message['To'] = Header(','.join(receivers), 'utf-8') 

                subject = mail_cfg['subject']
                message['Subject'] = Header(subject, 'utf-8')
                smtpObj = smtplib.SMTP_SSL(host, port)
                smtpObj.login(email_addr, passwd)
                smtpObj.sendmail(email_addr, receivers, message.as_string())
                sended = True
                logger.info("sendind successed")
                break
            except Exception as e:
                logger.error("sending failed: {}, retry {}...", e, retry)
                retry += 1
                time.sleep(retry_sleep)

        run_times += 1
        logger.info('run times {}, connected {}, sended {}, timer {}...', run_times, connected, sended, timer)
        if timer <= 1000:
            logger.info('timer <= 1000, run once, exit...')
            break
        time.sleep(timer)
    # return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--timer",
                        default=86400 * 3,
                        type=int,
                        help="send mail per timer(default 86400) seconds")
    args = parser.parse_args()
    notify = args.notify
    timer = args.timer

    username = cfg['user']['name']
    passwd = cfg['user']['password']
    delay = cfg['program']['delay']
    time.sleep(delay)
    # import pyvirtualdisplay
    # display = pyvirtualdisplay.Display(visible=0)
    # display.start()

    login_timer(username=username, passwd=passwd, timer=timer, notify=notify)
