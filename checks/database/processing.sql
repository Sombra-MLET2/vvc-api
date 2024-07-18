insert into categories(name, meta_name) values('Vinho Tinto', 'tinto'); -- 1
insert into categories(name, meta_name) values('Vinho Branco', 'branco'); -- 2
insert into categories(name, meta_name) values('Uvas de Mesa', 'mesa'); -- 3

insert into processings(cultivation, year, quantity, grape_class_id, category_id) values('Gewurztraminert', 2024, 575, 1, 3);
insert into processings(cultivation, year, quantity, grape_class_id, category_id) values('Alicante Bouschet', 2024, 1029, 2, 3);

select pro.cultivation, pro.year, pro.quantity, cat.name, cat_grap.name
from processings pro
         inner join categories cat on pro.category_id = cat.id
         inner join categories cat_grap on pro.grape_class_id = cat_grap.id;
/*
|              Wine | Year | Quantity | Type   | Class         |
|------------------:|-----:|---------:|--------|---------------|
| Alicante Bouschet | 2024 |     1029 | Tinto  | Uvas de Mesa  |
|   Gewurztraminert | 2024 |      575 | Branco | Uvas de Mesa  |
 */