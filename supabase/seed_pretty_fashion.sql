insert into business_settings (business_name, tax_id, currency_code, tax_rate)
values ('Pretty Fashion', null, 'CLP', 0.1900)
on conflict do nothing;

insert into branches (name, code)
values ('Casa Matriz', 'MAIN')
on conflict (code) do nothing;

insert into categories (name, slug)
values
    ('Sostenes', 'sostenes'),
    ('Calzones', 'calzones'),
    ('Conjuntos', 'conjuntos')
on conflict (slug) do nothing;

insert into attributes (name, slug)
values
    ('Talla', 'talla'),
    ('Copa', 'copa'),
    ('Color', 'color'),
    ('Tipo de prenda', 'tipo-prenda')
on conflict (slug) do nothing;

insert into attribute_values (attribute_id, value)
select id, value
from attributes
join (
    values
        ('talla', '32'),
        ('talla', '34'),
        ('talla', '36'),
        ('talla', '38'),
        ('copa', 'A'),
        ('copa', 'B'),
        ('copa', 'C'),
        ('copa', 'D'),
        ('color', 'Negro'),
        ('color', 'Blanco'),
        ('color', 'Beige'),
        ('tipo-prenda', 'Sosten'),
        ('tipo-prenda', 'Calzon'),
        ('tipo-prenda', 'Conjunto')
) as seed(slug, value) on seed.slug = attributes.slug
on conflict (attribute_id, value) do nothing;

insert into products (category_id, name, description)
select categories.id, seed.name, seed.description
from categories
join (
    values
        ('sostenes', 'Sosten basico', 'Sosten clasico de uso diario'),
        ('calzones', 'Calzon basico', 'Calzon clasico'),
        ('conjuntos', 'Conjunto basico', 'Conjunto de sosten y calzon')
) as seed(category_slug, name, description) on seed.category_slug = categories.slug
where not exists (
    select 1
    from products
    where products.name = seed.name
);

insert into product_attributes (product_id, attribute_id)
select products.id, attributes.id
from products
join attributes on attributes.slug in ('talla', 'color', 'tipo-prenda')
where products.name in ('Calzon basico')
on conflict do nothing;

insert into product_attributes (product_id, attribute_id)
select products.id, attributes.id
from products
join attributes on attributes.slug in ('talla', 'copa', 'color', 'tipo-prenda')
where products.name in ('Sosten basico', 'Conjunto basico')
on conflict do nothing;

insert into product_variants (product_id, sku, barcode, sale_price, cost_price)
select products.id, seed.sku, seed.barcode, seed.sale_price, seed.cost_price
from products
join (
    values
        ('Sosten basico', 'SOST-36-C-NEG', '7800000000011', 12990.00, 7000.00),
        ('Sosten basico', 'SOST-34-B-BLA', '7800000000012', 12990.00, 7000.00),
        ('Calzon basico', 'CALZ-M-NEG', '7800000000021', 5990.00, 2500.00),
        ('Conjunto basico', 'CONJ-36-C-BEI', '7800000000031', 18990.00, 10000.00)
) as seed(product_name, sku, barcode, sale_price, cost_price)
    on seed.product_name = products.name
on conflict (sku) do nothing;

insert into variant_attribute_values (variant_id, attribute_value_id)
select product_variants.id, attribute_values.id
from product_variants
join (
    values
        ('SOST-36-C-NEG', 'talla', '36'),
        ('SOST-36-C-NEG', 'copa', 'C'),
        ('SOST-36-C-NEG', 'color', 'Negro'),
        ('SOST-36-C-NEG', 'tipo-prenda', 'Sosten'),
        ('SOST-34-B-BLA', 'talla', '34'),
        ('SOST-34-B-BLA', 'copa', 'B'),
        ('SOST-34-B-BLA', 'color', 'Blanco'),
        ('SOST-34-B-BLA', 'tipo-prenda', 'Sosten'),
        ('CALZ-M-NEG', 'talla', '36'),
        ('CALZ-M-NEG', 'color', 'Negro'),
        ('CALZ-M-NEG', 'tipo-prenda', 'Calzon'),
        ('CONJ-36-C-BEI', 'talla', '36'),
        ('CONJ-36-C-BEI', 'copa', 'C'),
        ('CONJ-36-C-BEI', 'color', 'Beige'),
        ('CONJ-36-C-BEI', 'tipo-prenda', 'Conjunto')
) as seed(sku, attribute_slug, value)
    on seed.sku = product_variants.sku
join attributes on attributes.slug = seed.attribute_slug
join attribute_values
    on attribute_values.attribute_id = attributes.id
   and attribute_values.value = seed.value
on conflict do nothing;

insert into inventory (branch_id, variant_id, quantity, minimum_quantity, location)
select branches.id, product_variants.id, seed.quantity, seed.minimum_quantity, seed.location
from branches
join (
    values
        ('SOST-36-C-NEG', 10, 2, 'A1'),
        ('SOST-34-B-BLA', 8, 2, 'A1'),
        ('CALZ-M-NEG', 15, 3, 'B1'),
        ('CONJ-36-C-BEI', 6, 2, 'C1')
) as seed(sku, quantity, minimum_quantity, location) on true
join product_variants on product_variants.sku = seed.sku
where branches.code = 'MAIN'
on conflict (branch_id, variant_id) do nothing;
