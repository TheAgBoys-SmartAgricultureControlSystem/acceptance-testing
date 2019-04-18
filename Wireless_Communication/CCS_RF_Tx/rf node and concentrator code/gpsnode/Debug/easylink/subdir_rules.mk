################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
easylink/%.obj: ../easylink/%.c $(GEN_OPTS) | $(GEN_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/Users/Dhruva/workspace_v8/GPS Acceptance Test" --include_path="C:/ti/simplelink_cc13x2_sdk_2_30_00_45/source/ti/posix/ccs" --include_path="C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/include" --define=DeviceFamily_CC13X2 --define=CCFG_FORCE_VDDR_HH=0 -g --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --preproc_with_compile --preproc_dependency="easylink/$(basename $(<F)).d_raw" --obj_directory="easylink" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


