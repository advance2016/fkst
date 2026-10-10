# 文件路径：项目根目录/CMakeLists.txt

# 1. 指定 CMake 最低版本（必须放在最前面）
cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_COMPILER gcc)

# 2. 定义项目名称、版本和语言
project(MyProject)



# 3. 设置 C++ 标准为 C++17，并强制要求使用该标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 4. 添加静态库目标
add_library(MyLib STATIC
    src/lib/core.cpp      # 核心功能实现
    src/lib/helper.cpp    # 辅助函数实现
)

# 5. 添加可执行文件目标
add_executable(MyApp
    src/main.cpp           # 程序入口
    src/utils.cpp          # 工具函数
)

# 6. 为库目标指定公开头文件路径
#    PUBLIC 表示使用 MyLib 的目标也能访问该路径
target_include_directories(MyLib PUBLIC ${PROJECT_SOURCE_DIR}/include)

# 7. 为可执行文件指定私有头文件路径
target_include_directories(MyApp PRIVATE ${PROJECT_SOURCE_DIR}/src)

# 8. 将 MyLib 链接到 MyApp
target_link_libraries(MyApp PRIVATE MyLib)

# 9. 设置安装规则
install(TARGETS MyApp RUNTIME DESTINATION bin)
install(TARGETS MyLib ARCHIVE DESTINATION lib)