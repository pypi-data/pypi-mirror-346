# SmartPush_AutoTest



## Getting started

## 打包/上传的依赖（已安装不需要再次安装）
```sh
pip install wheel
pip install twine
```

## 1、清空本地文件夹

```sh
#!/bin/bash

# 定义要清空的目录和文件类型
BUILD_DIR="build"
DIST_DIR="dist"
EGG_INFO_PATTERN="*.egg-info"

# 清空 build 目录
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
    echo "成功删除 $BUILD_DIR 目录"
else
    echo "$BUILD_DIR 目录不存在"
fi

# 清空 dist 目录
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
    echo "成功删除 $DIST_DIR 目录"
else
    echo "$DIST_DIR 目录不存在"
fi

# 查找并删除所有 .egg-info 文件或目录
find . -name "$EGG_INFO_PATTERN" -exec rm -rf {} +
echo "已删除所有 $EGG_INFO_PATTERN 文件或目录"

```

## 2、更新版本号
```sh
#!/bin/bash
# 从 setup.py 文件中提取版本号
version=$(grep "version=" setup.py | sed -E "s/.*version=['\"]([^'\"]+)['\"].*/\1/")
# 将版本号拆分为数组
version_parts=($(echo "$version" | awk -F. '{for(i=1;i<=NF;i++) print $i}'))
# 获取版本号数组的长度
len=${#version_parts[@]}
# 输出拆分后的数组，用于调试
echo "拆分后的版本号数组: ${version_parts[@]}"
# 增加最后一位版本号
last_index=$((len))
((version_parts[$last_index]++))
# 处理进位
for ((i = last_index; i > 0; i--)); do
    if [ ${version_parts[$i]} -ge 10 ]; then
        version_parts[$i]=0
        ((version_parts[$i - 1]++))
    else
        break
    fi
done
# 重新组合版本号
new_version=$(IFS=. ; echo "${version_parts[*]}")
# 根据系统类型使用不同的 sed 命令
if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/version=['\"][^'\"]*['\"]/version='$new_version'/" setup.py
else
    sed -i "s/version=['\"][^'\"]*['\"]/version='$new_version'/" setup.py
fi
echo "版本号已从 $version 更新为 $new_version"
```


## 3、打包
```sh
python setup.py bdist_wheel
if [ $? -eq 0 ]; then
    echo "bdist_wheel 执行成功"
else
    echo "bdist_wheel 执行失败"
fi
```


## 4、上传到pipy的命令
```sh
twine upload dist/*
```

# 平台调用demo
```
import json # import 请置于行首
from smartpush.export.basic import ExcelExportChecker
from smartpush.export.basic import GetOssUrl
oss=GetOssUrl.get_oss_address_with_retry(vars['queryOssId'], "${em_host}", json.loads(requestHeaders))
result = ExcelExportChecker.check_excel_all(expected_oss=oss,actual_oss=vars['exportedOss'],ignore_sort =True)
assert result
```
## check_excel_all() 支持拓展参数
    1、check_type = "including"   如果需要预期结果包含可传  eg.联系人导出场景可用，flow导出场景配合使用
    2、ignore_sort = 0   如果需要忽略内部的行排序问题可传，eg.email热点点击数据导出无排序可用，传指定第几列，0是第一列
    3、ignore_sort_sheet_name = "url点击"   搭配ignore_sort使用，指定哪个sheet忽略排序，不传默认所有都排序，参数大小写不敏感(url点击-URL点击)
    4、skiprows = 1   传1可忽略第一行，   eg.如flow的导出可用，动态表头不固定时可以跳过读取第一行

## get_oss_address_with_retry(target_id, url, requestHeader, requestParam=None, is_import=False, **kwargs)
    1、is_import 导入校验是否成功传True,否则默认都是导出
    2、**kwargs 参数支持重试次数     
        tries = 30 # 重试次数
        delay = 2  # 延迟时间，单位s