from config.config import Config


if __name__ == '__main__':
    cfg = Config()
    print(cfg.cfg)
    cfg = Config('config/test')
    print(cfg.cfg)