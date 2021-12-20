import pyautogui as pg
import random as r
import pytesseract
import re

# pg.PAUSE = 1

pytesseract.pytesseract.tesseract_cmd = "D:\\Tesseract\\tesseract.exe"


def random_video():
    random = r.randrange(1, 9, 1)
    a = None
    b = None
    if random == 1:
        a = "1934"
        b = "254"
    if random == 2:
        a = "1934"
        b = "365"
    if random == 3:
        a = "1934"
        b = "509"
    if random == 4:
        a = "1934"
        b = "633"
    if random == 5:
        a = "1934"
        b = "792"
    if random == 6:
        a = "1934"
        b = "902"
    if random == 7:
        a = "1934"
        b = "1028"
    if random == 8:
        a = "1934"
        b = "1170"
    if random == 9:
        a = "1934"
        b = "1290"
    return a, b


def video_id():
    video_id_screenshot = pg.screenshot("Icons/id.png", region=(318, 45, 80, 17))
    video_id_str = pytesseract.image_to_string(video_id_screenshot)
    return video_id_str


def is_jem():
    local_position = pg.position()
    pg.screenshot("Icons/IsJam.png", region=(local_position.x +80, local_position.y - 80, 150, 80))
    if pg.locate("Icons/Djam.png", "Icons/IsJam.png"):
        return True
    return False



def is_stream():
    local_position = pg.position()
    pg.screenshot("Icons/IsStream.png", region=(local_position.x + 80, local_position.y + 30, 300, 80))
    if pg.locate("Icons/Stream.png", "Icons/IsStream.png"):
        return True
    return False


def new_count():
    i = 0
    for new in pg.locateAllOnScreen("Icons/NewVideo.png", confidence=0.9):
        i += 1
    return i


def channel_names():
    channel_name_str = {}
    video_num = 0
    for find_dot in pg.locateAllOnScreen("Icons/Dot.png", confidence=0.96):
        video_num += 1
        channel_name = ((find_dot.left - 150), (find_dot.top - 20), 250, 20)
        channel_name_screenshot = pg.screenshot("Icons/ChannelName.png", region=channel_name)
        channel_name_str.update(
            {video_num: pytesseract.image_to_string(channel_name_screenshot, lang='rus+eng', config='--psm 7')})
        channel_name_str = {k : re.sub(r'[@ \n]','', v) for k, v in channel_name_str.items()}
    return channel_name_str



def video_length():
    channel_duration_str = {}
    pg.moveTo(1937, 240)
    find_clock = pg.locateOnScreen("Icons/ClockImage.png", confidence=0.9)
    video_num = 0
    video_num += 1
    channel_duration = ((find_clock.left - 31), (find_clock.top + 80), 70, 30)
    channel_duration_screenshot = pg.screenshot("Icons/ChannelDuration.png", region=channel_duration)
    channel_duration_str.update(
        {video_num: pytesseract.image_to_string(channel_duration_screenshot, config='--psm 13 oem --3 tessedit_char_whitelist=0123456789:')})
    while find_clock is not None:
        local_position = pg.position()
        pg.moveTo(local_position.x, local_position.y + 133)
        find_clock = pg.locateOnScreen("Icons/ClockImage.png", confidence=0.8)
        if is_jem() or is_stream():
            local_position = pg.position()
            pg.moveTo(local_position.x, local_position.y + 133)
            find_clock = pg.locateOnScreen("Icons/ClockImage.png", confidence=0.8)
            video_num += 1
            channel_duration = ((find_clock.left - 32), (find_clock.top + 80), 70, 30)
            channel_duration_screenshot = pg.screenshot("Icons/ChannelDuration.png", region=channel_duration)
            channel_duration_str.update(
                {video_num: pytesseract.image_to_string(channel_duration_screenshot,
                                                        config='--psm 10 oem --3 tessedit_char_whitelist=0123456789:')})
            continue
        if find_clock is None:
            return channel_duration_str
        video_num +=1
        channel_duration = ((find_clock.left - 32), (find_clock.top + 80), 70, 30)
        channel_duration_screenshot = pg.screenshot("Icons/ChannelDuration.png", region=channel_duration)
        channel_duration_str.update(
                 {video_num: pytesseract.image_to_string(channel_duration_screenshot, config='--psm 10 oem --3 tessedit_char_whitelist=0123456789:', )})
    return channel_duration_str





def views_count():
    video_views_str = {}
    video_num = 0
    for find_dot in pg.locateAllOnScreen("Icons/Dot.png", confidence=0.96):
        video_num += 1
        video_views = ((find_dot.left - 152), find_dot.top + 5, 60, 20)
        video_views_screenshot = pg.screenshot("Icons/VideoViews.png", region=video_views)
        video_views_str.update(
            {video_num: pytesseract.image_to_string(video_views_screenshot, lang='rus', config='--psm 7')})
        video_views_str = {k : re.sub(r'[@ \n.]','', v) for k, v in video_views_str.items()}
    return video_views_str


def next_video():
    while True:
    #Кликаем на рандомное видео
        pg.leftClick(random_video())
    #Записываем количество рекомендованных видео
    #Тут пишется сколько объектов класса

    #Записываем названия видео
        print(channel_names())
    #Записываем количество просмотров
        print(views_count())
    #Записываем количество новинок
        print(new_count())
    #Записываем ID открытого видео
        print(video_id())
    #Записываем длинну видео
        print(video_length())

next_video()