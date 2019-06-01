-- create user test_user password 'test_password';
-- create database test owner test_user;

create type public.owner_type as enum ('direct', 'indirect');

CREATE SEQUENCE public.test_siquence START 1 MINVALUE 1 MAXVALUE 9223372036854775807;

create table public.stock_prices (
	"rn" bigint not null PRIMARY key DEFAULT nextval('test_siquence'),
	"company" varchar(50) not null,
	"date" date not null,
	"open" decimal(14,4) not null,
	"high" decimal(14,4) not null,
	"low" decimal(14,4) not null,
	"close" decimal(14,4) not null,
	"volume" int not null,
	CONSTRAINT ixu_stock_prices UNIQUE ("company", "date")
);

CREATE INDEX ix_stock_prices_company ON public.stock_prices USING btree ("company");
CREATE INDEX ix_stock_prices_date ON public.stock_prices USING btree ("date");

COMMENT ON TABLE public.stock_prices IS 'Цены акций';
COMMENT ON COLUMN public.stock_prices."company" IS 'Мнемокод компании';
COMMENT ON COLUMN public.stock_prices."date" IS 'Дата';
COMMENT ON COLUMN public.stock_prices."open" IS 'Цена на открытии дня';
COMMENT ON COLUMN public.stock_prices."high" IS 'Наивысшая цена';
COMMENT ON COLUMN public.stock_prices."low" IS 'Наименьшая цена';
COMMENT ON COLUMN public.stock_prices."close" IS 'Цена на закрытии дня';
COMMENT ON COLUMN public.stock_prices."volume" IS 'Количество';

create table public.insiders(
	"rn" bigint not null PRIMARY key DEFAULT nextval('test_siquence'),
	"company" varchar(50) not null,
	"name" varchar(255) not null,
	"relation" varchar(150) not null,
	CONSTRAINT ixu_insiders UNIQUE ("company", "name")
);

CREATE INDEX ix_insiders_company ON public.insiders USING btree ("company");

COMMENT ON TABLE public.insiders IS 'Инвесторы';
COMMENT ON COLUMN public.insiders."company" IS 'Мнемокод компании';
COMMENT ON COLUMN public.insiders."name" IS 'ФИО';
COMMENT ON COLUMN public.insiders."relation" IS 'Дожность';

create table public.trades (
	"rn" bigint not null PRIMARY key DEFAULT nextval('test_siquence'),
	"insider" bigint not null,
	"date" date not null,
	"type" varchar(255) not null,
	"owner_type" owner_type not null,
	"traded" int not null,
	"held" int not null,
	"price" decimal(14,4) not null,
	FOREIGN KEY ("insider") REFERENCES public.insiders ("rn") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX ix_trades_insider ON public.trades USING btree ("insider");

COMMENT ON TABLE public.trades IS 'Торговые операции';
COMMENT ON COLUMN public.trades."insider" IS 'Инвестор';
COMMENT ON COLUMN public.trades."date" IS 'Дата';
COMMENT ON COLUMN public.trades."type" IS 'Тип операции';
COMMENT ON COLUMN public.trades."owner_type" IS 'Тип владения';
COMMENT ON COLUMN public.trades."traded" IS 'Кол-во акций продажи';
COMMENT ON COLUMN public.trades."held" IS 'Кол-во акций удержаний';
COMMENT ON COLUMN public.trades."price" IS 'Цена';
