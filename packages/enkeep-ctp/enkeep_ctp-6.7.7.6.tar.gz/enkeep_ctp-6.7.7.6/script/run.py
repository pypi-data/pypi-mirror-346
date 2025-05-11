from enkeep_trade.event import EventEngine
from enkeep_trade.trader.engine import MainEngine
from enkeep_trade.trader.ui import MainWindow, create_qapp

from enkeep_ctp import CtpGateway


def main():
    """主入口函数"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
