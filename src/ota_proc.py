from main.ota_updater import OTAUpdater

#def download_and_install_update_if_available():
#    sleep(1)
#    print('check for new firmware version in github...')
#    o = OTAUpdater('https://github.com/winkste/mp32_generic')
#    o.check_for_update_to_install_during_next_reboot()
#    o.download_and_install_update_if_available('FRITZ!Box 7580 RU', '84757589397899114157')
#    sleep(5)

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/winkste/mp32_generic')
    if True == o.check_for_update():
        o.download_latest_released_version()
        #o.install_update()


#download_and_install_update_if_available()
