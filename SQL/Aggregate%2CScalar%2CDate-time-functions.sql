-- Aggregate Functions --

select sum(cost) as sum_of_all_costs from petrescue;
select max(quantity) as max_animals from petrescue;
select avg(cost) as average_cost from petrescue;
select avg(cost/quantity) as average_cost_dog from petrescue where animal = 'Dog';


--Scalar and String Functions --

select round(cost) as Rounded_cost from petrescue;
select length(animal) from petrescue;
select UNIQUE ucase(animal) from petrescue;
select * from petrescue where animal = 'Cat';

-- Date and Time Functions --

select month(rescuedate) from petrescue where animal = 'Cat';
select sum(quantity) from petrescue where month(rescuedate) = '5';
select sum(quantity) from petrescue where day(rescuedate) = '14';
select (rescuedate + 3 days) from petrescue;
select (current_date - rescuedate) from petrescue;