from func_update import Box


if __name__ == '__main__':
    box = Box()
    box.read_config()
    box.get_prize_rand()
    box.get_prize_normal()
    # box.detect_accelerator()
    box.main_loop()