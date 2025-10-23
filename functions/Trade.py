class Trade:
    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()
        assert self.config is not None

    def save_trade_locally(
        self, symbol, price, position, profit_limt, stop_loss, date_time, reason
    ):
        assert self.config.DB_Connection is not None
        db_conn = self.config.DB_Connection
        cursor = db_conn.cursor()

        try:
            cursor.execute(
                "insert  into Trades(symbol, price, position, profit_limit,  stop_loss , date_time , reason ) values(?, ?, ?, ?, ?, ?, ?)",
                (symbol, price, position, profit_limt, stop_loss, date_time, reason),
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
                "select symbol, price, position, profit_limit, stop_loss, date_time, reason from Trades where symbol = ?",
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
                mapped_trades.append(m_trade)
            return mapped_trades

        except Exception as e:
            return f"Error: Trying to get trades from db. \n{e}"
