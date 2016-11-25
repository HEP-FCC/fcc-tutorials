Github workflow and contribution guide
=========================

Contents
--------

-   [Overview](#overview)
-   [Generate and set up ssh keys for github](#generate-and-set-up-ssh-keys-for-github)
-   [Development workflow](#development-workflow)
-   [Recommendations](#recommendations)
-   [Trouble shooting](#trouble-shooting)
-   [Need help?](#need-help)

Overview
-------------

This page should allow new Git users to get started with the FCC
software, and describes the workflow for accessing and contributing FCC
code.

For a general introduction to git, have a look at these tutorials:

-   [Atlassian tutorial](https://www.atlassian.com/git/tutorials/)
-   [Interactive tutorial](http://pcottle.github.io/learnGitBranching/)
-   [The git book](https://git-scm.com/book/en/v2)

Generate and set up ssh keys for github
--------------------------------------------

When working on lxplus we recommend to clone github repositories via SSH, especially if you want to contribute code. For this to work, you need to generate ssh keys for authentication. See the corresponding github [help-page](https://help.github.com/articles/generating-an-ssh-key/).

> If you only want to use the software it may be easier to use https. In that case you don't need to generate the keys but have to replace `git@github:` with `https://github.com/` in all the instructions. Note that you'll not be able to push to your repository when you are on lxplus. You can also start using https for now and later re-add your repository with ssh authentication, see the [trouble shooting section](#trouble-shooting)



Development workflow
-------------------------

You will be using (at least) 3 versions of the FCCSW repository:

1.  The official [FCCSW on github](https://github.com/HEP-FCC/FCCSW)
2.  Your fork of FCCSW on github (see [github help](https://help.github.com/articles/fork-a-repo/) on what that means)
3.  Your local repository copy in your work area (e.g. on AFS)

The repositories 1 and 2 are added as remote to the repository 3:

```bash
git clone git@github.com:[YOUR_GITHUB_USER]/FCCSW.git
cd FCCSW
git remote add hep-fcc git@github.com:HEP-FCC/FCCSW.git
```

To get new code, do the following in 3

-   fetch information from 1

    ```bash
    git fetch hep-fcc
    ```

-   merge the master branch from 1 into your development area do

    ```bash
    git merge hep-fcc/master
    ```

-   push your local changes to 2 (see below how to create a local branch)

    ```
    git push origin [NAME_OF_LOCAL_BRANCH]
    ```

To contribute new code, do the following:

-   develop your feature in 3 on a local branch of your choice, to create a branch do:

    ```
    git branch -b [NAME_OF_LOCAL_BRANCH]
    ```

-   get new code from 1 as explained above and merge it in this branch
-   test:
    -   that the code compiles and all tests succeed (`make; make test`)
    -   that your code runs
    -   that it produces the expected results
    -   [add tests for your code](https://github.com/HEP-FCC/FCCSW/blob/master/doc/AddingTestsToFCCSW.md)
-   push your local branch to 2 (see above)
-   create a pull request from 2 to 1 (see github [help-page](https://help.github.com/articles/creating-a-pull-request/) )

Recommendations
--------------------

Please always follow the recommendations below:

-   feel free to commit often to your local repository, but do not
    create pull request for small incremental changes
-   if you're working on a given topic, always create a branch for
    it, e.g. pythia\_interface. You may commit many times to this branch
    in your local repository. When you have something solid create a
    pull request to the official FCCSW repository.
-   always provide a meaningful comment for each commit
-   commit comments should look like the one below, so that they show up
    correctly in git printouts.

    ```
    first version of a pythia interface # this line should be a short 1 liner

    Here, you may write a few more lines if needed
    ```

- You may also want to have a look at our [coding guidelines](https://github.com/HEP-FCC/FCCSW/blob/master/doc/CppCodingStyleGuidelines.md).

Trouble-shooting
----------------

### When I try to push to the repository, I get an authentication error

Check with `git remote -v` which remote repositories you have added to your local copy. You should see something like:

```
hep-fcc	git@github.com:HEP-FCC/FCCSW.git (fetch)
hep-fcc	git@github.com:HEP-FCC/FCCSW.git (push)
origin	git@github.com:[your git user name]/FCCSW.git (fetch)
origin	git@github.com:[your git user name]/FCCSW.git (push)
```

If you see something similar but all the addresses start with `https`, see [below](#i-have-cloned-with-https-and-now-i-cant-push-my-changes-what-do-i-do).

If you only see `origin git@github.com:HEP-FCC/FCCSW.git`, you need to add your own repository, push to that and do a pull request, as described above. To add your own repository do:

```
git remote rename origin hep-fcc
git remote add myfccsw git@github.com:[your git user name]/FCCSW.git
```


### I have cloned with https and now I can't push my changes, what do I do?

You only need to re-add your repository as a remote with ssh authentication:

```
git remote add myfccsw_ssh git@github.com:[your git user name]/FCCSW.git
```

Now you can push to that remote with:

```
git push myfccsw_ssh [the branch you want to push]
```

Need help?
---------------

In case you have any question on this tutorial, or need help to sort out
an issue with a repository, Feel free to drop a mail to
fcc-experiments-sw-dev at CERN, and we'll be happy to help you
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")
!
