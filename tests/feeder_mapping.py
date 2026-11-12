"""The derivation feeder mapping as the suite states it at Step 13.

This table states, per starter metric, the feeder record kinds its
derivation reads as feeders, apart from any cross check. The metrics
record stands as a feeder for one derivation only, D-1, and only in
the shrunk D-09 form the entry states. For every other derivation the
metrics record, where it holds a figure, is a cross check only and
never a feeder. Step 14 binds the product feeder mapping to this
table; the binding duty is carried in the Step 13 record.
"""

METRICS_RECORD = "metrics record"

FEEDER_MAP = {
    "T-1": ("path ledger transition log",),
    "T-2": ("path ledger transition log",),
    "T-4": ("path ledger banked states", "decision queue file"),
    "T-7": ("gate verdict records", "step records"),
    "E-1": ("step records", "roster artifacts"),
    "E-2": ("step records", "roster artifacts"),
    "E-3": ("cost ledger token figures",),
    "E-4": ("cost ledger money figures", "step records"),
    "F-2": ("gate records", "gate rulings", "gate adjudications"),
    "Q-1": ("audit round records", "gate adjudications"),
    "Q-3": ("defect registers", "audit records"),
    "Q-4": ("first trace records", "gate records"),
    "D-1": (METRICS_RECORD,),
    "B-1": ("metric rows T-1 and T-2",),
    "B-2": ("cost ledger money figures", "cost ledger token figures"),
    "B-3": ("metric rows T-1 and T-2",),
    "B-4": ("metric rows T-1 and T-2",),
}

D1_FEEDER_CONDITION = (
    "metrics record decision table only, and only where no "
    "DECISION-QUEUE.md file in the named form stands, under decision "
    "D-09 as shrunk by proposal WV-12; where such a queue file "
    "stands, the queue file is the feeder and the decision table is "
    "the cross check")
