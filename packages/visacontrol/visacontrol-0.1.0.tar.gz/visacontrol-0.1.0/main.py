import pyvisa
import time
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("visacontrol")

connected_instruments = {}


@mcp.tool()
def connect_instrument(self, ip_address: str):
    try:
        if ip_address in connected_instruments:
            return {"status": "success", "identity": connected_instruments[ip_address]["identity"]}

        # Use pyvisa-py backend
        rm = pyvisa.ResourceManager('@py')
        resource = f'TCPIP::{ip_address}::5025::SOCKET'

        instrument = rm.open_resource(resource)
        instrument.timeout = 10000  # 10 seconds timeout
        instrument.write_termination = '\n'
        instrument.read_termination = '\n'

        # Verify connection with *IDN?
        identity = instrument.query('*IDN?').strip()
        connected_instruments[ip_address] = {
            "resource_manager": rm,
            "instrument": instrument,
            "identity": identity
        }
        return {"status": "success", "identity": identity}
    except Exception as e:
        return {"error": f"Failed to connect to {ip_address}: {str(e)}"}

@mcp.tool()
def execute_command(self, ip_address: str, command: str):
    try:
        if ip_address not in connected_instruments:
            return {"error": f"Device {ip_address} not connected"}

        instrument = connected_instruments[ip_address]["instrument"]
        instrument.write(command)
        time.sleep(0.5)  # Allow command to process
        return {"status": "success", "message": f"Command '{command}' executed"}
    except Exception as e:
        return {"error": f"Command execution failed: {str(e)}"}

@mcp.tool()
def query_instrument(self, ip_address: str, query: str):
    try:
        if ip_address not in connected_instruments:
            return {"error": f"Device {ip_address} not connected"}

        instrument = connected_instruments[ip_address]["instrument"]
        result = instrument.query(query).strip()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"error": f"Query failed: {str(e)}"}

@mcp.tool()
def disconnect_instrument(self, ip_address: str):
    try:
        if ip_address in connected_instruments:
            connected_instruments[ip_address]["instrument"].close()
            connected_instruments[ip_address]["resource_manager"].close()
            del connected_instruments[ip_address]
            return {"status": "success", "message": "Device disconnected"}
        else:
            return {"error": f"Device {ip_address} not connected"}
    except Exception as e:
        return {"error": f"Disconnect failed: {str(e)}"}

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')