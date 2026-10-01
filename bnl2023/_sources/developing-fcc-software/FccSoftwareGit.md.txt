# Github workflow and contribution guide



## Overview

This page should allow users that are new to Git to get started with the FCC
software, and describes the workflow for accessing and contributing FCC
code.

For a general introduction to git, have a look at these tutorials:

-   [Atlassian tutorial](https://www.atlassian.com/git/tutorials/)
-   [Interactive tutorial](http://pcottle.github.io/learnGitBranching/)
-   [The git book](https://git-scm.com/book/en/v2)

## First time setup of git

Please refer to [this tutorial](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) and the [GitHub help](https://help.github.com/articles/set-up-git/).

## Generate and set up ssh keys for github

When working on lxplus we recommend to clone github repositories via SSH, especially if you want to contribute code. For this to work, you need to generate ssh keys for authentication. See the corresponding github [help-page](https://help.github.com/articles/generating-an-ssh-key/).

:::{admonition} Generate and set up ssh keys for github
:class: callout

 If you only want to use the software it may be easier to use https. In that case you don't need to generate the keys but have to replace `git@github:` with `https://github.com/` in all the instructions. Note that you'll not be able to push to your repository when you are on lxplus. You can also start using https for now and later re-add your repository with ssh authentication, see the [trouble shooting section](#trouble-shooting)
:::


## Improving your git experience

It may be useful to install [Git integration tools](https://github.com/git/git/tree/master/contrib/completion) for your shell that allow tab-completion of most git commands and also can show you in your prompt on which branch you currently are, what changes you have pending, etc.

## Development workflow

You will be using (at least) 3 versions of the FCCSW repository:

1.  The official [FCCSW on github](https://github.com/HEP-FCC/FCCSW)
2.  Your fork of FCCSW on github (see [github help](https://help.github.com/articles/fork-a-repo/) on what that means)
3.  Your local repository copy in your work area (e.g. on AFS)

The repositories 1 and 2 are added as remote to the repository 3:

```bash
git clone git@github.com:[YOUR_GITHUB_USER]/FCCSW.git # create a local copy (3) of your fork (2)
cd FCCSW
git remote add hep-fcc git@github.com:HEP-FCC/FCCSW.git # add official repo (1) as additional remote
```

### Keeping your local repository up to date

-   fetch all changes from the official repository (1)

    ```bash
    git fetch hep-fcc
    ```

-   rebase your development area to the master branch from the official repository (1), **please read [this](https://www.atlassian.com/git/tutorials/rewriting-history) to avoid loss of work**

    ```bash
    git rebase -i hep-fcc/master
    ```

    in this process you can also fix any commits that need touching up, **be aware that deleting commits in the list will result also in the deletion of the corresponding changes** (more info in the [GitHub help](https://help.github.com/articles/about-git-rebase/) and the [Atlassian tutorial](https://www.atlassian.com/git/tutorials/rewriting-history))

-   push your local changes to your fork (2), see [below](#contributing-code) how to create a local branch

    ```
    git push origin [NAME_OF_LOCAL_BRANCH]
    ```

### Contributing code

-   if you are fixing a bug, first create an issue in the github [issue tracker](https://github.com/HEP-FCC/FCCSW/issues)
-   develop your feature in your local copy (3) on a local branch of your choice, to create a branch do:

    ```
    git branch -b [NAME_OF_LOCAL_BRANCH]
    ```

-   refer to [this tutorial](https://www.atlassian.com/git/tutorials/saving-changes) to see how to commit changes
-   occasionally, get new code from the official repository (1) as explained above and merge it in this branch
-   test:
    -   that the code compiles and all tests succeed (`make && make test`)
    -   that your code runs (even better: [add an automatic test](https://github.com/HEP-FCC/FCCSW/blob/master/doc/AddingTestsToFCCSW.md))
    -   that it produces the expected results
-   push your local branch to your fork (2) (see [above](#keeping-your-local-repository-up-to-date))
-   create a pull request from your fork (2) to the offical repository's (1) master branch (see github [help-page](https://help.github.com/articles/creating-a-pull-request/))
    - also see the [recommendations for pull requests](#pull-requests)

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

### Pull requests

- Give a meaningful title that appropriately describes what you did (e.g. Add new calorimeter clustering)
  - Pull requests of work in progress (to make people aware that you are working on a feature) create a PR starting with "[WIP]"
- In the description, give a short bullet-point list of what was done
- If your pull request fixes issues tracked in the [issue tracker](https://github.com/HEP-FCC/FCCSW/issues):
    - Make sure you added a test that shows they are actually fixed
    - In the description mention that you fixed it by referring to the issue: "fixes #<issue-id>" (this will automatically close the issue, see also [GitHub help](https://help.github.com/articles/closing-issues-via-commit-messages/))

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

---

## Need help?

In case you have any questions on this guide, or need help to sort out
an issue with a repository, feel free to drop a mail to
fcc-experiments-sw-dev at CERN, and we'll be happy to help you.
Alternatively create an issue in the [bug tracker](https://github.com/HEP-FCC/FCCSW/issues)
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")
