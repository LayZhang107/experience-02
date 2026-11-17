# GitHub 留痕操作

在本目录执行以下命令即可保留实验二的版本过程：

```bash
git init
git add README.md skills schemas src data/sample docs/experiment02.md
git commit -m "v0.1: add consumer insight specification and sample data"
git add tests data/generated docs/blind_test_record.md
git commit -m "v0.2: add blind tests, failure revisions, and reproducible generator"
git tag v0.2
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main --tags
```

不要把真实账号、Token、个人敏感信息或绕过访问限制的代码提交到仓库。提交后把仓库 URL、两个 commit、tag `v0.2` 和盲测记录链接填入课程作业。 
