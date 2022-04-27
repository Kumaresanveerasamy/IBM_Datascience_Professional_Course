-- creating a view 

create view employee_info as
select  EMP_ID, F_NAME, L_NAME, B_DATE, SEX, SALARY from employees;

-- replace a view

create or replace view employee_info as 
select  EMP_ID, F_NAME, L_NAME, SEX from employees;

--drop a view
 
drop view employee_info 