CREATE TABLE public.type_of_jobs (
	id_type_of_jobs int4 NOT NULL,
	"name" varchar(40) NULL,
	CONSTRAINT type_of_jobs_pkey PRIMARY KEY (id_type_of_jobs)
);


CREATE TABLE public.employee (
	id_employee int4 NOT NULL,
	"name" varchar(20) NOT NULL,
	surname varchar(20) NOT NULL,
	patronymic varchar(20) NOT NULL,
	rate float4 NOT NULL,
	CONSTRAINT employee_pkey PRIMARY KEY (id_employee)
);


CREATE TABLE public.company (
	id_company integer PRIMARY KEY,
	"name" varchar(150) NOT NULL,
	UNP integer NOT NULL
);



CREATE TABLE public."month" (
	id_month integer PRIMARY KEY,
	start_date date NOT NULL,
	end_date date NOT NULL,
	count_of_working_days integer NOT NULL,
	number_of_employees float4 NOT NULL
);


CREATE TABLE public.service_agreement (
	id_agreement integer PRIMARY KEY,
	"number" varchar(30) NOT NULL,
	amount money NOT NULL,
	id_type_of_jobs integer NOT NULL,
	id_company integer NOT NULL,
	
	CONSTRAINT fk_type_of_jobs
      FOREIGN KEY(id_type_of_jobs) 
	  REFERENCES type_of_jobs(id_type_of_jobs),
	
	CONSTRAINT fk_company
      FOREIGN KEY(id_company) 
	  REFERENCES company(id_company)
	 
);


CREATE TYPE public.status AS ENUM ('completed', 'not completed');
CREATE TABLE public.act_of_completed_work (
	id_act integer PRIMARY KEY,
	stage_number integer NOT NULL,
	amount money NOT NULL,
	man_hours float4 NOT NULL,
	"status" status,
	id_employee integer NOT NULL,
	id_month integer NOT NULL,
	id_agreement integer NOT NULL,
	
	CONSTRAINT fk_employee
      FOREIGN KEY(id_employee) 
	  REFERENCES employee(id_employee),
	
	CONSTRAINT fk_month
      FOREIGN KEY(id_month) 
	  REFERENCES "month"(id_month),
	
	CONSTRAINT fk_service_agreement
      FOREIGN KEY(id_agreement) 
	  REFERENCES service_agreement(id_agreement)
);

CREATE TABLE public.month_job (
	id_job integer PRIMARY KEY,
	man_hours float4 NOT NULL,
	id_employee integer NOT NULL,
	id_month integer NOT NULL,
	id_act integer NOT NULL,
	
	CONSTRAINT fk_employee
      FOREIGN KEY(id_employee) 
	  REFERENCES employee(id_employee),
	
	CONSTRAINT fk_month
      FOREIGN KEY(id_month) 
	  REFERENCES "month"(id_month),
	
	CONSTRAINT fk_act_of_completed_work
      FOREIGN KEY(id_act) 
	  REFERENCES act_of_completed_work(id_act)
);
