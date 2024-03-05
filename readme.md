## Server and Nodes for weather monitoring

Nodes (ESP microcontroller) with attached sensors (temperature, humidity, ..) regulary measure environment and send data to server, in our case Raspberry PI via UDP.
Server stores measurements in sqlite DB.

### server

setup sqlite:
  ```sh
create table nodes(id integer not null primary key, mac text, ip text, module text);
create table measurements(id integer primary key, temperature double, humidity double, node integer not null, timestamp text, epoch integer, foreign key (node) references nodes (id));
  ```

### nodes

