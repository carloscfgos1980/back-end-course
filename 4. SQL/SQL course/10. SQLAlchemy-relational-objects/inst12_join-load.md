## Joined Load
The joinedload() eager load strategy is the oldest eager loader in SQLAlchemy, which augments the SELECT statement that’s being passed to the database with a JOIN (which may be an outer or an inner join depending on options), which can then load in related objects.

The joinedload() strategy is best suited towards loading related many-to-one objects, as this only requires that additional columns are added to a primary entity row that would be fetched in any case. For greater efficiency, it also accepts an option joinedload.innerjoin so that an inner join instead of an outer join may be used for a case such as below where we know that all Address objects have an associated User:

>>> from sqlalchemy.orm import joinedload
>>> stmt = (
...     select(Address)
...     .options(joinedload(Address.user, innerjoin=True))
...     .order_by(Address.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.Address.email_address} {row.Address.user.name}")
SELECT address.id, address.email_address, address.user_id, user_account_1.id AS id_1,
user_account_1.name, user_account_1.fullname
FROM address
JOIN user_account AS user_account_1 ON user_account_1.id = address.user_id
ORDER BY address.id
[...] ()
spongebob@sqlalchemy.org spongebob
sandy@sqlalchemy.org sandy
sandy@squirrelpower.org sandy
pearl.krabs@gmail.com pkrabs
pearl@aol.com pkrabs

joinedload() also works for collections, meaning one-to-many relationships, however it has the effect of multiplying out primary rows per related item in a recursive way that grows the amount of data sent for a result set by orders of magnitude for nested collections and/or larger collections, so its use vs. another option such as selectinload() should be evaluated on a per-case basis.

It’s important to note that the WHERE and ORDER BY criteria of the enclosing Select statement do not target the table rendered by joinedload(). Above, it can be seen in the SQL that an anonymous alias is applied to the user_account table such that is not directly addressable in the query. This concept is discussed in more detail in the section The Zen of Joined Eager Loading.

The ON clause rendered by joinedload() may be affected directly by using the PropComparator.and_() method described previously at Augmenting the ON Criteria; examples of this technique with loader strategies are further below at Augmenting Loader Strategy Paths. However, more generally, “joined eager loading” may be applied to a Select that uses Select.join() using the approach described in the next section, Explicit Join + Eager load.

Tip

It’s important to note that many-to-one eager loads are often not necessary, as the “N plus one” problem is much less prevalent in the common case. When many objects all refer to the same related object, such as many Address objects that each refer to the same User, SQL will be emitted only once for that User object using normal lazy loading. The lazy load routine will look up the related object by primary key in the current Session without emitting any SQL when possible.