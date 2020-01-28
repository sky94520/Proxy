create table proxy (
    ip varchar(32) not null,
    port int not null primary key (ip, port)
);