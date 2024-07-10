// mysql database
create database data;

use data;

create table data.batch (
	batch_id varchar(256),
	current_status varchar(256),
	no_of_processed int,
	final_status varchar(256)
);


create table data.process_image(
	batch_id varchar(256),
	image_url varchar(256)
	);

SELECT  * FROM data.batch ;