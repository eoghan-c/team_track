<?php
	//ini_set('display_errors',1);
	//error_reporting(E_ALL);

	// Database login details
	$servername = "localhost";
	$username   = "[SQL USER]";
	$password   = "[SQL USER PASSWORD]";
	$db         = "[SQL DATABASE]";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $db);

	// Check connection
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	}

	// Define useful variables
	$target_height = 3408;
	$height_achieved = 0;

	// Calculate the height everyone has already reached
	$sql = "SELECT SUM(`walls`.`height`) AS `height_achieved` FROM `walls` RIGHT JOIN `readings` on `walls`.`reader_id` = `readings`.`reader_id`";
	$result = $conn->query($sql) or trigger_error(mysql_error()." ".$sql);
	if ($result) {
		if ($result->num_rows > 0) {
		    // output data of each row
		    while($row = $result->fetch_assoc()) {
		    	if (!is_null($row["height_achieved"]))
		        	$height_achieved = $row["height_achieved"];
		    }
		}
	}

	// Calculate the individual totals
	$sql = "SELECT `people`.`name` AS `person_name`, SUM(`walls`.`height`) AS `total_height` FROM `people` JOIN `readings` on `people`.`tag_id` = `readings`.`tag_id` JOIN `walls` on `readings`.`reader_id` = `walls`.`reader_id` GROUP BY `people`.`name` ORDER BY `total_height` DESC";
	$result = $conn->query($sql) or trigger_error(mysql_error()." ".$sql);

	$person_leaderboard = [];
	if ($result) {
		if ($result->num_rows > 0) {
		    // output data of each row
		    while($row = $result->fetch_assoc()) {
		        $person_leaderboard[] = [$row["person_name"], $row["total_height"]];
		    }
		}
	}

	$height_remaining = $target_height - $height_achieved;
	$height_remaining_percent = round($height_achieved / $target_height * 100);

	// Cope with us going over our target height
	$height_remaining_msg = "Height remaining:";
	if ($height_remaining < 0) {
		$height_remaining_msg = "** TARGET ACHIEVED! **";
		$height_remaining = "plus " + abs($height_remaining);
	}

	// Report the values
echo <<< EOT
	<table id="overall">
		<tr>
			<td>Target height:</td><td>{$target_height} m</td>
		</tr>
		<tr>
			<td>Height climbed:</td><td>{$height_achieved} m ({$height_remaining_percent}%)</td>
		</tr>
		<tr>
			<td class="height_remaining">{$height_remaining_msg}</td><td class="height_remaining">{$height_remaining} m</td>
		</tr>
	</table>

	<hr class="separator">

	<table id="leaderboard">
EOT;
	foreach ($person_leaderboard as $curr_person) {
echo <<< EOT
		<tr>
			<td>{$curr_person[0]}:</td><td>{$curr_person[1]} m</td>
		</tr>
EOT;
	}
echo <<< EOT
	</table>
EOT;

	$conn->close();
?>
