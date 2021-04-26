-- auto-generated definition
drop table if exists PaymentSystem_systemusers;
drop table if exists PaymentSystem_transaction;
create table PaymentSystem_users
(
    id            integer      not null
        constraint table_name_pk
            primary key autoincrement,
    username      varchar(255) not null,
    password      varchar(255) not null,
    wallet_number bigint       not null,
    total         int default 5000 not null
);

create unique index table_name_id_uindex
    on PaymentSystem_users (id);

create unique index table_name_wallet_number_uindex
    on PaymentSystem_users (wallet_number);



-- auto-generated definition
create table PaymentSystem_transaction
(
    id                     integer not null
        constraint PaymentSystem_transaction_pk
            primary key autoincrement,
    sender_wallet_number   integer not null,
    receiver_wallet_number int     not null,
    transaction_amount     int     not null
);

create unique index PaymentSystem_transaction_id_uindex
    on PaymentSystem_transaction (id);

