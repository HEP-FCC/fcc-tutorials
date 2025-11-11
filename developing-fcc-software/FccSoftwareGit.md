# Github workflow and contribution guide

[TOC]

## Introduction

This page should allow users that are new to Git to get started with the FCC
software, and describes the workflow for accessing and contributing FCC
code.

For a general introduction to git, have a look at these tutorials:

-   [Atlassian tutorial](https://www.atlassian.com/git/tutorials/)
-   [Interactive tutorial](https://pcottle.github.io/learnGitBranching/)
-   [The git book](https://git-scm.com/book/en/v2)

### First time setup of git

Set global information about you, particularly your name and email. This information will be attached to each commit and it will be visible to other contributors. To do it, please use the following commands
```bash
git config --global user.name "Name Family-name"
git config --global user.email "Name.Family-name@cern.ch"
```

Please refer to [this tutorial](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) and the [GitHub help](https://help.github.com/articles/set-up-git/).

### Generate and set up ssh keys for github

When working on lxplus we recommend to clone github repositories via SSH, especially if you want to contribute code. For this to work, you need to generate ssh keys for authentication. See the corresponding github [help-page](https://help.github.com/articles/generating-an-ssh-key/).

:::{admonition} Generate and set up ssh keys for github
:class: callout

 If you only want to use the software it may be easier to use https. In that case you don't need to generate the keys but have to replace `git@github:` with `https://github.com/` in all the instructions. Note that you'll not be able to push to your repository. You can also start using https for now and later re-add your repository with ssh authentication, see the [trouble shooting section](#trouble-shooting)
:::


### Improving your git experience

It may be useful to install [Git integration tools](https://github.com/git/git/tree/master/contrib/completion) for your shell that allow tab-completion of most git commands and also can show you in your prompt on which branch you currently are, what changes you have pending, etc.

Other tools with a graphical interface are available, e.g., `git-gui`, `git-cola`, `gitkraken` (which present the main Git commands as buttons, shows differences between commits, etc.) and `tig` (a terminal-based tool that graphically displays the Git commit history). Most editors have dedicated plugins as well (magit for emacs, vim-fugitive for vim, etc).

## How to contribute

This section covers the main commands to contribute to an open project via Pull Requests. See [TLDR section](TL;DR) for a summary.

### Understanding repositories

You will be using (at least) 3 versions of a repository, two on GitHub and a local copy in your machine:

1.  The official on GitHub, e.g. [FCCSW on github](https://github.com/HEP-FCC/FCCSW)
2.  Your fork on GitHub (see [github help](https://help.github.com/articles/fork-a-repo/) on what that means)
3.  Your local repository copy in your work area

The repositories 1 and 2 are added as remote to the repository 3. Let's start by creating a local copy of a dummy repository called `key4hep_repo`, from the `key4hep` organization

```bash
git clone git@github.com:[YOUR_GITHUB_USER]/key4hep_repo.git
```

That command links the local copy to the remote repository. The default name of this remote repository is `origin`. Let's add the official repository as remote too, but with a different name. The usual convention is to name the official repository `upstream`:
```bash
cd FCCSW
git remote add upstream https://github.com/key4hep/key4hep_repo.git
```

### Development workflow

This section explains how to use a locally installed package instead of the one provided in the stack, make changes to it, and contribute those changes to the official repository.

A recommended zero step is to open an issue in the corresponding repository, e.g. [in FCCSW repository](https://github.com/HEP-FCC/FCCSW/issues).

#### Source the software stack

We need to source the software stack before starting the actual development, e.g.,
```bash
# nightlies
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# release
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

The sourcing of stacks accepts arguments:
* -r <year-month-day>, for a specific date
* -d, for packages compiled with debug symbols
* -h or -help, for help related to the usage and arguments

#### Branching

The development should happen in a dedicated branch of your personal repository (2), forked from the official repository (1). To download a local copy of your personal fork, run the following command:
```bash
git clone git@github.com:[YOUR_GITHUB_USER]/key4hep_repo.git
```

Move to the new directory,
```bash
cd key4hep_repo
```

Create a new branch for the feature you are developing. This branch is created now on your local copy of the repository. We will have to update the GitHub repository later.
```bash
git checkout -b new_feature_branch
```

Now we are ready to start developing the actual changes.

#### Creating changes

Let's replace locally the official repository in the stack by our local copy. To do so, configure (first line), build and install (second line) your local copy of the repository, and then redefine the bash environmental variables to point to your local copy (third line). This is achieved by the following code:
```bash
cmake -B build -S . -D CMAKE_INSTALL_PREFIX=install
cmake --build build -- -j 4  install
k4_local_repo
```

#### Create commits and run tests

Modify files as needed for your development. Ideally, each meaninful change should correspond to a commit. Before adding a new commit, it is recommend to run some kind of test (at least that it compiles and run without errors; running ctest would be highly desirable), otherwise there is a risk of leaving the repository in a so-called `broken state`. The following lines show how to mark for commiting, so called `stage`, the files `file1`, `file2` and `README` (first line), and then creating a commit (second line). The commit message should make the change in the files understandable to other developers.
```bash
git add file1 README
git commit -m "new awesome feature"
```
Refer to [this tutorial](https://www.atlassian.com/git/tutorials/saving-changes) further details about commiting in Git.

:::{admonition}
If the feature is completely new in the repository, it is advisable to add a new ctest. Since there is not a standard in Key4hep, it is easier to ask the maintainer of the corresponding repository how to do it. See the following [link](https://github.com/HEP-FCC/FCCSW/blob/master/doc/AddingTestsToFCCSW.md) for further details
:::

Once all your changes are ready, please run the ctests. To do so, go to the build directory and run `ctest` as follows.
```bash
cd build
ctest
```

:::{admonition}
If you want to integrate changes in the official repository (1) happening while you are developing, [the next section](#keeping-your-local-repository-up-to-date)) show how to update your local repository, in such a manner that your changes (git commits) are reallocated on top of the newest changes from the official repository (so-called `rebasing`).
:::

Then, we push the changes of our local repository in the development branch `new_feature_branch` to the personal fork in GitHub (named `origin`) by doing the following
```bash
git push origin new_feature_branch
```

### Opening a Pull Request (PR)

Once we have pushed the changes into a new branch of our fork, we are ready to open a Pull Request. If we now go to the GitHub page of the repository, `https://github.com/[YOUR_GITHUB_USER]/key4hep_repo`, a banner asking if we want to open a Pull request should appear. If not, look for a button called `Contribute`, and click on `Open pull request`. Please check the [following section](Pull-Request-description) for a list of tasks to be fullfilled before opening a PR.


### After merging the Pull Request

After the PR is merged you will have to update (_rebase_) the main branch in the forked repository, **not the feature branch**. The following commands will update the local copy of the main branch with the `upstream/main` branch, and then push the changes to the forked repository

```
git fetch upstream -p --all
git checkout main
git rebase upstream/main
git push
```

## Recommendations

Please always follow the recommendations below.

### General recommendations

-   if you're working on a given topic, always create a branch for
    it, e.g. `pythia_interface`. You may commit many times to this branch
    in your local repository. When you have something solid create a
    pull request to the official FCCSW repository.
- Have a look at our [coding guidelines](https://github.com/HEP-FCC/FCCSW/blob/master/doc/CppCodingStyleGuidelines.md).

### Commit comments

-   feel free to commit often to your local repository, make a pull request once the topic you are working on is finished
    - if the feature you are working on is large, consider making a work in progress-pull request (see [below](#pull-requests))
    - git commits represent a snapshot of the software as a whole, and not only the difference to a previous commit (although that as well, in practice). It is recommended that each commit compiles and passes the tests. Take a look at the [commit history of FCCSW](https://github.com/HEP-FCC/FCCSW/commits/master) and the histories of some individual files to find both good and bad examples. 
    
-   always provide a meaningful comment for each commit
    -   if you are working on an issue, refer to that issue by adding "refs. #[issue id]", see also
        [GitHub help](https://help.github.com/articles/closing-issues-via-commit-messages/)
-   commit comments should look like the one below, so that they show up
    correctly in git printouts.

    ```
    first version of a pythia interface # this line should be a short 1 liner

    Here, you may write a few more lines if needed
    ```
### Pull Request description

When opening a new Pull Request, please fill the following information in text box.

1. Please fill a short description what your PR is changing, to be added in the release notes of the repository. This text has the following syntax
```
BEGINRELEASENOTES
- New/Extends XXX
- Fixes issue XXX

ENDRELEASENOTES
```

2. In the description, give a short bullet-point list of what was done. If your PR is fixing an open Issue in GitHub, please
- include the link to it.
- Make sure you added a test that shows they are actually fixed
- In the description mention that you fixed it by referring to the issue: "fixes #<issue-id>" (this will automatically close the issue, see also [GitHub help](https://help.github.com/articles/closing-issues-via-commit-messages/))


:::{admonition}
There are number of requisites that will speed up the revision of the Pull request
* Give a meaningful title that appropriately describes what you did (e.g. Add new calorimeter clustering)
* Pull requests of work in progress (to make people aware that you are working on a feature) create a PR starting with "[WIP]"
* Sufficiently documented code (inline, doxygenm, readmes...)
* Tests cover the modified code
* The branch is up to date (see [next section](Keeping-your-local-repository-up-to-date) about how to do it)
* The pull request only contains minimal necesary changes

In case of modifying detector-related code, please check the following as well:
* Overlap test, [link](https://hep-fcc.github.io/fcc-tutorials/main/full-detector-simulations/Geometry/Geometry.html#overlap-checking)
* Simulation test, run with a particle gun of your choice, e.g. [link](https://hep-fcc.github.io/fcc-tutorials/main/full-detector-simulations/Geometry/Geometry.html#modify-an-existing-xml-file)
:::

### Keeping your local repository up to date

It may happen that your fork or development branch becomes outdated with respect to the main branch in the official (`upstream`) repository (1). To update your development branch of your forked repository, please follow these steps:

1. Fetch all changes from the official repository (1)
```bash
git fetch upstream
```

2. Rebase your development branch onto the latest main branch from the upstream repository
Some repositories have renamed the `master` branch to `main`. Use autocompletion or check on GitHub to confirm.

```bash
git rebase -i upstream/master
```

During the rebase process, you may encounter conflicts if you have modified the same file that has already been changed in the main repository. **Do not panic!** Read carefully the terminal messages and follow their instructions.

#### Handling Merge Conflicts
For each conflict:
1. Open the corresponding file.
2. Look for the conflicting code marked with `>>>`, `===`, and `<<<` symbols.
3. Edit the file to resolve the conflict (removing the conflict markers may be enough, but ensure the correct changes are kept).
4. Save the changes.
5. Inform Git that the file is ready by running:
   ```bash
   git add <file_name>
   ```
6. Continue the rebase process with:
   ```bash
   git rebase --continue
   ```
7. If necessary, repeat these steps until the rebase is complete.

If something goes wrong and you need to cancel the rebase, you can run:
```bash
git rebase --abort
```

During this process, you can also fix any commits that need modification. **Be aware that deleting commits from the list will also delete the corresponding changes.** More information can be found in the [GitHub help](https://help.github.com/articles/about-git-rebase/) and the [Atlassian tutorial](https://www.atlassian.com/git/tutorials/rewriting-history).

For further details on how to avoid loss of work, **please read [this guide](https://www.atlassian.com/git/tutorials/rewriting-history)**.

3. Push your local changes to your fork (2)

```bash
git push --set-upstream origin [NAME_OF_LOCAL_BRANCH]
```

where the option `--set-upstream` sets up tracking so that future `git pull` and `git push` commands will automatically reference `origin/[NAME_OF_LOCAL_BRANCH]`

:::{admonition}
GitHub web interface allows to update (rebase) and solve simple merge conflicts as well, see [link](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github)
:::

### Cleaning history

- before opening a pull request it may be a good idea to check that your history makes sense (commit messages explain what you did, no unnecessary commits, etc.), check with:

  ```
  git log
  ```
- if you see commits that you'd like to change, there are several ways of doing that, the most commonly used is `git rebase`:
    - with the interactive version you can rebase your development branch to the official master and fix the history at the same time

    ```
    git fetch hep-fcc # get changes from the official repo
    git rebase -i hep-fcc/master # do the actual rebase
    ```

    - git will guide you through the steps, where you can delete entire commits (and the corresponding changes), merge commits and change commit messages
    - more information can be found in [this tutorial](https://www.atlassian.com/git/tutorials/rewriting-history#git-rebase-i)



## Trouble-shooting

### When I try to push to the repository, I get an authentication error

Check with `git remote -v` which remote repositories you have added to your local copy. You should see something like:

```
hep-fcc	git@github.com:HEP-FCC/FCCSW.git (fetch)
hep-fcc	git@github.com:HEP-FCC/FCCSW.git (push)
origin	git@github.com:[your git user name]/FCCSW.git (fetch)
origin	git@github.com:[your git user name]/FCCSW.git (push)
```

If you see something similar but all the addresses start with `https`, see [below](#i-have-cloned-with-https-and-now-i-cant-push-my-changes-what-do-i-do).

If you only see `origin git@github.com:HEP-FCC/FCCSW.git`, you need to add your own repository, push to that one and do a pull request, as described above. To add your own repository do:

```
git remote rename origin hep-fcc
git remote add myfccsw git@github.com:[your git user name]/FCCSW.git
```


### I have cloned with https and now I can't push my changes, what do I do?

You only need to change the URL of your remote pointing to your repository to one that uses SSH instead:

```
git remote set-url [the remote name] git@github.com:[your git user name]/FCCSW.git
```

Now you can push to that remote with:

```
git push [the remote name] [the branch you want to push]
```

## TL;DR

```bash
# Clone your fork of the key4hep repository locally
git clone git@github.com:atolosadelgado/key4hep_repo
cd key4hep_repo

# Create a new branch for the feature you are developing
git checkout -b new_feature_branch

# Modify files
git add file1 file2... Readme
git commit -m "new feature"

# Run ctest before pushing (ideally before committing)

# Push the new branch to your fork
git push origin new_feature_branch

# Ready to open a PR on GitHub
```

If you need to rebase your development branch with the latest changes from
key4hep central repository (so-called `upstream`):

```bash
# Add the upstream repository
git remote add upstream https://github.com/key4hep/key4hep_repo.git

# Fetch the latest changes from upstream
git fetch upstream

# Rebase your development branch onto the latest main branch (resolve conflicts if needed)
git rebase upstream/main

# Push updated branch (use --force-with-lease to avoid overwriting unintended changes)
git push --force-with-lease
```

---

## Need help?

In case you have any questions on this guide, or need help to sort out
an issue with a repository, feel free to drop a mail to
fcc-experiments-sw-dev at CERN, and we'll be happy to help you.
Alternatively create an issue in the [bug tracker](https://github.com/HEP-FCC/FCCSW/issues)
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")
