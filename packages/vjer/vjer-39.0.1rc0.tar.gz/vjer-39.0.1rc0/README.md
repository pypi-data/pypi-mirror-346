# Vjer Python Module

A command line tool for automating CI/CD tasks.

## Developing

Development is best accomplished using virtualenv or virtualenv-wrapper where a virtual environment can be generated:

    UNIX: util/new-env.sh
    Windows: util\New-Env.ps1

To update the current development environment

    UNIX: util/update-env.sh
    Windows: util\Update-Env.ps1

## Testing

The test suite can be run with

    vjer test

## Building

The build can be run with

    vjer build

## Publishing a Release

This is the procedure for releasing Vjer

1. Validate that all issues are "Ready for Release".
1. Update CHANGELOG.md.
1. Run the Publish workflow against the Production environment.
1. Validate the GitHub release and tag.
1. Validate PyPi was published properly.
1. Label the issues as res::complete and mark as "Completed".
1. Close the Milestone.
1. Update the source in Perforce.
1. If this was a release branch, merge to master.

<!--- cSpell:ignore vjer virtualenv -->
