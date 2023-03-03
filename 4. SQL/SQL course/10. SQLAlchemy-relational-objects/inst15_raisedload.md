## Raiseload
One additional loader strategy worth mentioning is raiseload(). This option is used to completely block an application from having the N plus one problem at all by causing what would normally be a lazy load to raise an error instead. It has two variants that are controlled via the raiseload.sql_only option to block either lazy loads that require SQL, versus all “load” operations including those which only need to consult the current Session.

One way to use raiseload() is to configure it on relationship() itself, by setting relationship.lazy to the value "raise_on_sql", so that for a particular mapping, a certain relationship will never try to emit SQL:

class User(Base):
    __tablename__ = "user_account"

    # ... Column mappings

    addresses = relationship("Address", back_populates="user", lazy="raise_on_sql")


class Address(Base):
    __tablename__ = "address"

    # ... Column mappings

    user = relationship("User", back_populates="addresses", lazy="raise_on_sql")

Using such a mapping, the application is blocked from lazy loading, indicating that a particular query would need to specify a loader strategy:

u1 = s.execute(select(User)).scalars().first()
u1.addresses
sqlalchemy.exc.InvalidRequestError: 'User.addresses' is not available due to lazy='raise_on_sql'

The exception would indicate that this collection should be loaded up front instead:

u1 = s.execute(select(User).options(selectinload(User.addresses))).scalars().first()

The lazy="raise_on_sql" option tries to be smart about many-to-one relationships as well; above, if the Address.user attribute of an Address object were not loaded, but that User object were locally present in the same Session, the “raiseload” strategy would not raise an error.