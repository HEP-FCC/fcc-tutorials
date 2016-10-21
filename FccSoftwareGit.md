---
layout: site
---
[]() Git for the FCC software
=============================

Contents

-   [Git for the FCC software](#git-for-the-fcc-software)
    -   [Overview](#overview)
    -   [FCC Git tutorial](#fcc-git-tutorial)
    -   [Generate and set up ssh keys for
        github](#generate-and-set-up-ssh-keys-for)
    -   [Development workflow](#development-workflow)
    -   [Recommendations](#recommendations)
    -   [Need help?](#need-help)

[]() Overview
-------------

This page should allow new Git users to get started with the FCC
software, and describes the workflow for accessing and contributing FCC
code.

For a general introduction to git, have a look at these tutorials:

-   [Atlassian tutorial](https://www.atlassian.com/git/tutorials/)
-   [Interactive tutorial](http://pcottle.github.io/learnGitBranching/)
-   [The git book](https://git-scm.com/book/en/v2)

[]() FCC Git tutorial
---------------------

-   [Test git repository with tutorial
    instructions](https://github.com/HEP-FCC/GitTutorial) (might
    be outdated)

[]() Generate and set up ssh keys for github
--------------------------------------------

See the corresponding github
[help-page](https://help.github.com/articles/generating-an-ssh-key/)

[]() Development workflow
-------------------------

You will be using (at least) 3 versions of the FCCSW repository:

1.  The official FCCSW on github
2.  Your fork of FCCSW on github
3.  Your local repository on AFS

The repositories 1 and 2 are added as remote to the repository 3:

    git clone git@github.com:[YOUR_GITHUB_USER]/FCCSW.git
    cd FCCSW
    git remote add hep-fcc git@github.com:HEP-FCC/FCCSW.git

To get new code, do the following in 3

-   fetch information from 1

<!-- -->

       git fetch hep-fcc

-   merge 1/master into a local branch of your choice

<!-- -->

       git merge hep-fcc/master

-   push your local branch to 2

<!-- -->

       git push origin [NAME_OF_LOCAL_BRANCH]

To contribute new code, do the following:

-   develop your feature in 3 on a local branch of your choice
-   get new code from 1 as explained above and merge it in this branch
-   test:
    -   that the code compiles and all tests succeed (
        `      make; make test     ` )
    -   that your code runs
    -   that it produces the expected results
    -   [add tests for your
        code](https://github.com/HEP-FCC/FCCSW/blob/master/doc/AddingTestsToFCCSW.md)
-   push your local branch to 2 (see above)
-   create a pull request from 2 to 1 (see github
    [help-page](https://help.github.com/articles/creating-a-pull-request/) )

[]() Recommendations
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

<!-- -->

    first version of a pythia interface # this line should be a short 1 liner 

    Here, you may write a few more lines if needed

[]() Need help?
---------------

In case you have any question on this tutorial, or need help to sort out
an issue with a repository, Feel free to drop a mail to
fcc-experiments-sw-dev at CERN, and we'll be happy to help you
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")
!

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 08 Sep 2014
