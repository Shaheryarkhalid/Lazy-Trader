from datetime import datetime, timezone
from internals.Config import Config
from helpers import Singleton


@Singleton
class Trade:
    def __init__(self) -> None:
        self.config = Config()
        self.config.validate_config()
        assert self.config is not None

    def save_trade_locally(
        self,
        trade_id,
        symbol,
        price,
        position,
        profit_limt,
        stop_loss,
        reason,
    ):
        date_time = datetime.now(timezone.utc).isoformat()
        assert self.config.DB_Connection is not None
        db_conn = self.config.DB_Connection
        cursor = db_conn.cursor()

        try:
            cursor.execute(
                "insert  into Trades(trade_id, symbol, price, position, profit_limit,  stop_loss , date_time , reason ) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    trade_id,
                    symbol,
                    price,
                    position,
                    profit_limt,
                    stop_loss,
                    date_time,
                    reason,
                ),
            )
            db_conn.commit()
            return "Successfully saved trade in db."

        except Exception as e:
            return f"Error: Trying to save Trade in db. \n{e}"

    def get_trades_from_db(self, symbol):
        assert self.config.DB_Connection is not None
        db_conn = self.config.DB_Connection
        cursor = db_conn.cursor()

        try:
            cursor.execute(
                "select  symbol, price, position, profit_limit, stop_loss, date_time, reason, trade_id from Trades where symbol = ?",
                (symbol,),
            )
            trades = cursor.fetchall()
            mapped_trades = []
            for trade in trades:
                m_trade = {}
                m_trade["symbol"] = trade[0]
                m_trade["price"] = trade[1]
                m_trade["position"] = trade[2]
                m_trade["profit_limit"] = trade[3]
                m_trade["stop_loss"] = trade[4]
                m_trade["date_time"] = trade[5]
                m_trade["reason"] = trade[6]
                m_trade["trade_id"] = trade[7]
                mapped_trades.append(m_trade)
            return mapped_trades

        except Exception as e:
            return f"Error: Trying to get trades from db. \n{e}"
