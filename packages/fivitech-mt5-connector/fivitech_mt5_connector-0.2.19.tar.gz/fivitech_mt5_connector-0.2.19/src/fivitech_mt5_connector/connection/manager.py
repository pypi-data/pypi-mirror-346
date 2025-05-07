import logging
from typing import Optional, Dict, List
import MT5Manager
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from ..constants import MT5ServerConfig
from ..exceptions import MT5ConnectionError
from ..sinks import MT5UserSink, MT5DealSink, MT5PositionSink, MT5OrderSink, MT5SummarySink, MT5TickSink, MT5BookSink

logger = logging.getLogger(__name__)

# Default retry settings for connection attempts
DEFAULT_RETRY_STOP = stop_after_attempt(3)
DEFAULT_RETRY_WAIT = wait_exponential(multiplier=1, min=1, max=10)

class MT5ConnectionManager:
  def __init__(self, server_config: MT5ServerConfig, data_folder: Optional[str] = None):
    """
    Initialize MT5 Connection Manager
    
    Args:
      server_config: Server configuration containing connection details
      data_folder: Optional custom data folder path for MT5Manager
    """
    self.server_config = server_config
    self._manager = MT5Manager.ManagerAPI(data_folder) if data_folder else MT5Manager.ManagerAPI()
    self._admin = MT5Manager.AdminAPI(data_folder) if data_folder else MT5Manager.AdminAPI()
    self._connected = False
    self._user_sink: Optional[MT5UserSink] = None
    self._deal_sink: Optional[MT5DealSink] = None
    self._position_sink: Optional[MT5PositionSink] = None
    self._order_sink: Optional[MT5OrderSink] = None
    self._summary_sink: Optional[MT5SummarySink] = None
    self._tick_sink: Optional[MT5TickSink] = None # Corrected indentation
    self._book_sink: Optional[MT5BookSink] = None # Corrected indentation

  @retry(stop=DEFAULT_RETRY_STOP, wait=DEFAULT_RETRY_WAIT, reraise=True)
  def connect(self) -> bool:
    """
    Attempts to connect to MT5 server using configured IPs with failover and retries.
    Connects both ManagerAPI and AdminAPI instances.

    Raises:
        MT5ConnectionError: If connection fails after all retries.
        RetryError: If retries are exhausted (captured and re-raised as MT5ConnectionError).
    """
    if self._connected:
      return True
        
    for ip in self.server_config.ips:
      try:  
        # Connect ManagerAPI
        manager_result = self._manager.Connect(
          ip,
          self.server_config.username,
          self.server_config.manager_password,
          MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL,
          15000  # 1 minute timeout
        )
        print(f"ManagerAPI connection result: {manager_result}")
        if not manager_result:
          continue

        if self.server_config and getattr(self.server_config, 'connect_admin', False):
          # Connect AdminAPI with the same credentials
          admin_result = self._admin.Connect(
            ip,
            self.server_config.username,
            self.server_config.manager_password,
            MT5Manager.AdminAPI.EnPumpModes.PUMP_MODE_FULL,
            15000  # 1 minute timeout
          )
          print(f"AdminAPI connection result: {admin_result}")
          if not admin_result:
            # Disconnect manager if admin connection fails
            self._manager.Disconnect()
            continue
            
        self._connected = True
        return True
              
      except Exception as e:
        # Log the specific error for this IP attempt before continuing
        print(f"Connection Failed attempt: {ip}, error: {e}")
        logger.warning(f"Connection attempt failed for IP {ip} on server {self.server_config.name}: {e}. Last MT5 Error: {MT5Manager.LastError()}")
        # Ensure both are disconnected if either fails before trying the next IP
        try:
            self._manager.Disconnect()
        except Exception as disconnect_err:
            logger.debug(f"Ignoring manager disconnect error during connect attempt: {disconnect_err}")
        try:
            self._admin.Disconnect()
        except Exception as disconnect_err:
            logger.debug(f"Ignoring admin disconnect error during connect attempt: {disconnect_err}")
        continue # Try the next IP

    # If the loop completes without returning True, all IPs failed for this attempt
    raise MT5ConnectionError(
        f"Failed to connect to any IP for server {self.server_config.name} on this attempt. "
        f"Last MT5 error: {MT5Manager.LastError()}"
    )
      
  def disconnect(self):
    """
    Safely disconnect from MT5 server (both ManagerAPI and AdminAPI)
    """
    if self._connected:
      if self._user_sink:
        self._manager.UserUnsubscribe(self._user_sink)
      if self._deal_sink:
        self._manager.DealUnsubscribe(self._deal_sink)
      try:
        self._manager.Disconnect()
      except:
        pass
      try:
        self._admin.Disconnect()
      except:
        pass
      self._connected = False
          
  @property
  def manager(self) -> MT5Manager.ManagerAPI:
    """
    Returns active ManagerAPI instance
    
    Raises:
        MT5ConnectionError: If not connected to MT5 server
    """
    if not self._connected:
      raise MT5ConnectionError("Not connected to MT5 server")
    return self._manager
  
  @property
  def admin(self) -> MT5Manager.AdminAPI:
    """
    Returns active AdminAPI instance
    
    Raises:
        MT5ConnectionError: If not connected to MT5 server
    """
    if not self._connected:
      raise MT5ConnectionError("Not connected to MT5 server")
    return self._admin

  def check_health(self) -> bool:
    """
    Performs a simple check to verify the connection is active.

    Returns:
        bool: True if the connection is healthy, False otherwise.
    """
    if not self._connected:
        return False
    try:
        # TimeServerRequest is a lightweight call to check server responsiveness
        server_time = self._manager.TimeServerRequest()
        # Could add more checks here if needed, e.g., check admin connection
        return server_time is not None
    except Exception as e:
        logger.warning(f"Health check failed for server {self.server_config.name}: {e}")
        # Consider disconnecting if health check fails consistently
        # self.disconnect() # Optional: Force disconnect on health check failure
        return False

  def __enter__(self):
    """Context manager entry"""
    self.connect()
    return self
      
  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit"""
    self.disconnect()
    
  def setup_user_sink(self, sink: MT5UserSink) -> bool:
    """Setup user event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._user_sink:
      self._manager.UserUnsubscribe(self._user_sink)
    
    self._user_sink = sink
    return self._manager.UserSubscribe(sink)
    
  def setup_deal_sink(self, sink: MT5DealSink) -> bool:
    """Setup deal event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._deal_sink:
      self._manager.DealUnsubscribe(self._deal_sink)
    
    self._deal_sink = sink
    return self._manager.DealSubscribe(sink)
  
  def setup_position_sink(self, sink: MT5PositionSink) -> bool:
    """Setup position event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._position_sink:
      self._manager.PositionUnsubscribe(self._position_sink)

    self._position_sink = sink
    return self._manager.PositionSubscribe(sink)

  def setup_order_sink(self, sink: MT5OrderSink) -> bool:
    """Setup order event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._order_sink:
      self._manager.OrderUnsubscribe(self._order_sink)

    self._order_sink = sink
    return self._manager.OrderSubscribe(sink)
  
  def setup_summary_sink(self, sink: MT5SummarySink) -> bool:
    """Setup summary event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._summary_sink:
      self._manager.SummaryUnsubscribe(self._summary_sink)

    self._summary_sink = sink
    return self._manager.SummarySubscribe(sink)

  def setup_tick_sink(self, sink: MT5TickSink) -> bool:
    """Setup tick event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._tick_sink:
      self._manager.TickUnsubscribe(self._tick_sink)

    self._tick_sink = sink
    return self._manager.TickSubscribe(sink)

  def setup_book_sink(self, sink: MT5BookSink) -> bool:
    """Setup book event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._book_sink:
      self._manager.BookUnsubscribe(self._book_sink)

    self._book_sink = sink
    return self._manager.BookSubscribe(sink)

class MT5ConnectionPool:
  def __init__(self, server_configs: List[MT5ServerConfig], data_folder: Optional[str] = None):
    """
    Initialize MT5 Connection Pool
    
    Args:
      server_configs: List of server configurations
      data_folder: Optional custom data folder path for MT5Manager
    """
    self.connections: Dict[str, MT5ConnectionManager] = {}
    self.data_folder = data_folder
    
    for config in server_configs:
      self.connections[config.name] = MT5ConnectionManager(config, data_folder)
  
  def connect_all(self) -> Dict[str, bool]:
    """
    Attempts to connect to all configured MT5 servers
    Returns dict of server names and their connection status
    """
    results = {}
    for name, connection in self.connections.items():
      try:
        connection.connect()
        results[name] = True
      except MT5ConnectionError as e:
        results[name] = False
    return results
  
  def disconnect_all(self):
    """
    Disconnects from all MT5 servers
    """
    for connection in self.connections.values():
      connection.disconnect()
  
  def get_connection(self, server_name: str) -> MT5ConnectionManager:
    """
    Get connection manager for specific server
    
    Args:
      server_name: Name of the server to get connection for
        
    Raises:
      KeyError: If server name doesn't exist
    """
    if server_name not in self.connections:
      raise KeyError(f"No connection found for server: {server_name}")
    return self.connections[server_name]
  
  def __enter__(self):
    """Context manager entry"""
    self.connect_all()
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit"""
    self.disconnect_all()
