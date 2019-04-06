CREATE TABLE IF NOT EXISTS chatlog (
id SERIAL PRIMARY KEY,
msg_time INTEGER NOT NULL,
msg_type VARCHAR(16) NOT NULL,
client_id INTEGER NOT NULL,
client_name VARCHAR(32) NOT NULL,
client_team SMALLINT NOT NULL,
msg VARCHAR(528) NOT NULL,
target_id INTEGER DEFAULT NULL,
target_name VARCHAR(32) DEFAULT NULL,
target_team SMALLINT DEFAULT NULL,
FOREIGN KEY(client_id) REFERENCES clients(id));

CREATE TABLE IF NOT EXISTS cmdlog (
id SERIAL PRIMARY KEY,
cmd_time INTEGER NOT NULL,
admin_id INTEGER NOT NULL,
admin_name VARCHAR(32) NOT NULL,
command VARCHAR(100) NOT NULL,
data VARCHAR(528) DEFAULT NULL,
result VARCHAR(528) DEFAULT NULL,
FOREIGN KEY(admin_id) REFERENCES clients(id));