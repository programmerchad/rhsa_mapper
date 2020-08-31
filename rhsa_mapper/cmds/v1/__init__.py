from rhsa_mapper.cmds.v1.advisory import advisory
from rhsa_mapper.cmds.v1.cpes import cpe
from rhsa_mapper.cmds.v1.repos import repo


all_cmds = [
    advisory,
    repo,
    cpe
]
