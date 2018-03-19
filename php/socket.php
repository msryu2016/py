<?

// don¡¯t timeout
set_time_limit (0);
header("Content-Type: text/html; charset=UTF-8");


// set some variables
$host = "172.10.13.52";
$port = 12354;



// create socket
$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not createsocketn");

// bind socket to port
$result = socket_bind($socket, $host, $port) or die("Could not bind tosocketn");

// start listening for connections
$result = socket_listen($socket, 3) or die("Could not set up socketlistenern");

// accept incoming connections
// spawn another socket to handle communication
$spawn = socket_accept($socket) or die("Could not accept incomingconnectionn");

// keep looping and looking for client input
do
{
	// read client input
	$input = socket_read($spawn, 1024, 1) or die("Could not read inputn");

	if (trim($input) != ¡°¡±)
	{
		echo "Received input: $input\n";

		// if client requests session end
		if (trim($input) == ¡°END¡±)
		{
			// close the child socket
			// break out of loop
			socket_close($spawn);
			break;
		}
		// otherwise¡¦
		else
		{
			// reverse client input and send back  	$output = strrev($input) . ¡°n¡±;
			socket_write($spawn, $output . "? ", strlen (($output)+2)) or die(" 	echo ¡°Sent output: " . trim($output) . "\n");
		}
	}

} while (true);


// read client input
//$input = socket_read($spawn, 1024) or die("Could not read inputn");

// clean up input string
//$input = trim($input);

// reverse client input and send back
//$output = strrev($input) . "\n";
//socket_write($spawn, $output, strlen ($output)) or die("Could not writeoutputn");

// close sockets
socket_close($spawn);
socket_close($socket);

?>