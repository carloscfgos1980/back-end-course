## Committing
There’s much more to say about how the Session works which will be discussed further. For now we will commit the transaction so that we can build up knowledge on how to SELECT rows before examining more ORM behaviors and features:

>>> session.commit()
COMMIT

The above operation will commit the transaction that was in progress. The objects which we’ve dealt with are still attached to the Session, which is a state they stay in until the Session is closed (which is introduced at Closing a Session).

Tip

An important thing to note is that attributes on the objects that we just worked with have been expired, meaning, when we next access any attributes on them, the Session will start a new transaction and re-load their state. This option is sometimes problematic for both performance reasons, or if one wishes to use the objects after closing the Session (which is known as the detached state), as they will not have any state and will have no Session with which to load that state, leading to “detached instance” errors. The behavior is controllable using a parameter called Session.expire_on_commit. More on this is at Closing a Session.