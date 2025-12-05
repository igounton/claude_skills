#!/usr/bin/env bash
#
# linux_development_workstation_tuning.sh
#
# Optimizes Linux system parameters for modern development workstations.
# Addresses common issues with IDEs, file watchers, containers, and build tools.
#
# Usage:
#   sudo ./linux_development_workstation_tuning.sh [apply [--save] [--force]|status [--all]|reset]
#
# Commands:
#   apply [--save] [--force] - Apply tuning optimizations temporarily (use --save to persist)
#                              --force overwrites existing settings when using --save
#   status [--all]           - Show current vs recommended values (--all shows all config files)
#   reset|uninstall          - Remove persistent configuration files
#

set -euo pipefail

# Color output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Configuration file paths
readonly SYSCTL_CONF="/etc/sysctl.d/99-dev-workstation.conf"
readonly LIMITS_CONF="/etc/security/limits.d/99-dev-workstation.conf"
readonly SYSCTL_DIR="/etc/sysctl.d"
readonly LIMITS_DIR="/etc/security/limits.d"

# Tuning parameters - integrated from all existing configs
declare -A SYSCTL_PARAMS=(
    # Inotify limits for file watching (IDEs, build tools, etc.)
    ["fs.inotify.max_user_watches"]="524288"
    ["fs.inotify.max_user_instances"]="512"
    ["fs.inotify.max_queued_events"]="32768"

    # File descriptor limits
    ["fs.file-max"]="2097152"

    # AIO limits for databases and build tools
    ["fs.aio-max-nr"]="1048576"

    # Memory management (from 90-memory-optimization.conf)
    ["vm.swappiness"]="10"
    ["vm.vfs_cache_pressure"]="50"
    ["vm.dirty_ratio"]="15"
    ["vm.dirty_background_ratio"]="5"
    ["vm.min_free_kbytes"]="131072"
    ["vm.max_map_count"]="1048576"
    ["vm.oom_kill_allocating_task"]="0"
    ["vm.overcommit_memory"]="0"

    # Network tuning (integrated from multiple sources)
    ["net.core.somaxconn"]="4096"
    ["net.core.default_qdisc"]="fq_codel"
    ["net.ipv4.tcp_max_syn_backlog"]="4096"
    ["net.ipv4.conf.default.rp_filter"]="2"
    ["net.ipv4.conf.all.rp_filter"]="2"

    # Shared memory for containers and databases
    ["kernel.shmmax"]="17179869184" # 16GB
    ["kernel.shmall"]="4194304"     # 16GB in pages
)

# Track conflicts
declare -A CONFLICTS
declare -A CONFLICT_FILES

# Error handling
error() {
    echo -e "${RED}ERROR: $*${NC}" >&2
    exit 1
}

info() {
    echo -e "${BLUE}INFO: $*${NC}"
}

success() {
    echo -e "${GREEN}SUCCESS: $*${NC}"
}

warning() {
    echo -e "${YELLOW}WARNING: $*${NC}"
}

notice() {
    echo -e "${CYAN}NOTICE: $*${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)"
    fi
}

# Get current kernel parameter value
get_current_value() {
    local param="$1"
    sysctl -n "$param" 2>/dev/null || echo "unknown"
}

# Scan sysctl.d directory for existing parameter definitions
scan_for_conflicts() {
    local force_mode="$1"

    info "Scanning $SYSCTL_DIR for existing parameter definitions..."

    # Clear conflict tracking
    CONFLICTS=()
    CONFLICT_FILES=()

    # Scan all .conf files except our own
    for conf_file in "$SYSCTL_DIR"/*.conf; do
        [[ ! -f "$conf_file" ]] && continue
        [[ "$conf_file" == "$SYSCTL_CONF" ]] && continue

        # Parse file for parameter definitions
        while IFS= read -r line; do
            # Skip comments and empty lines
            [[ "$line" =~ ^[[:space:]]*# ]] && continue
            [[ "$line" =~ ^[[:space:]]*$ ]] && continue

            # Match parameter = value or parameter=value
            if [[ "$line" =~ ^[[:space:]]*([a-zA-Z0-9._-]+)[[:space:]]*=[[:space:]]*(.+)$ ]]; then
                local param="${BASH_REMATCH[1]}"
                local value="${BASH_REMATCH[2]}"

                # Check if this parameter is in our list
                if [[ -v "SYSCTL_PARAMS[$param]" ]]; then
                    CONFLICTS["$param"]="$value"
                    CONFLICT_FILES["$param"]="$conf_file"
                fi
            fi
        done <"$conf_file"
    done

    # Report conflicts
    if [[ ${#CONFLICTS[@]} -gt 0 ]]; then
        echo ""
        warning "Found ${#CONFLICTS[@]} parameter(s) already defined in other files:"
        echo ""

        for param in "${!CONFLICTS[@]}"; do
            local existing_value="${CONFLICTS[$param]}"
            local file_path="${CONFLICT_FILES[$param]}"
            local recommended_value="${SYSCTL_PARAMS[$param]}"

            if [[ "$existing_value" == "$recommended_value" ]]; then
                echo -e "${GREEN}  ✓ ${NC}${param} = ${existing_value}  ${CYAN}# Already correct in $(basename "$file_path")${NC}"
            else
                echo -e "${YELLOW}  ! ${NC}${param} = ${existing_value}  ${CYAN}# Found in $(basename "$file_path") (recommended: ${recommended_value})${NC}"
            fi
        done

        echo ""

        if [[ "$force_mode" != "true" ]]; then
            notice "Conflicting parameters will be SKIPPED unless you use: apply --force"
            return 1
        else
            warning "Force mode enabled - will override existing settings"
            return 0
        fi
    else
        success "No conflicts found - all parameters are available"
        return 0
    fi
}

# Show all sysctl and limits config files
show_all_configs() {
    info "All sysctl.d Configuration Files"
    echo ""

    local files=("$SYSCTL_DIR"/*.conf)

    for conf_file in "${files[@]}"; do
        [[ ! -f "$conf_file" ]] && continue

        local basename
        basename=$(basename "$conf_file")

        echo -e "${CYAN}=== ${basename} ===${NC}"
        cat "$conf_file"
        echo ""
    done

    info "All limits.d Configuration Files"
    echo ""

    local limit_files=("$LIMITS_DIR"/*.conf)

    for conf_file in "${limit_files[@]}"; do
        [[ ! -f "$conf_file" ]] && continue

        local basename
        basename=$(basename "$conf_file")

        echo -e "${CYAN}=== ${basename} ===${NC}"
        cat "$conf_file"
        echo ""
    done
}

# Show status of all parameters
show_status() {
    local show_all="${1:-false}"

    if [[ "$show_all" == "true" ]]; then
        show_all_configs
        return
    fi

    info "Current System Configuration vs Recommended Values"
    echo ""
    printf "%-45s %-15s %-15s %-10s\n" "PARAMETER" "CURRENT" "RECOMMENDED" "STATUS"
    printf "%s\n" "$(printf '=%.0s' {1..90})"

    local all_good=true

    for param in "${!SYSCTL_PARAMS[@]}"; do
        local current
        current=$(get_current_value "$param")
        local recommended="${SYSCTL_PARAMS[$param]}"

        local status="OK"
        local color="$GREEN"

        if [[ "$current" == "unknown" ]]; then
            status="UNKNOWN"
            color="$YELLOW"
            all_good=false
        elif [[ "$current" != "$recommended" ]]; then
            # Try numeric comparison
            if [[ "$current" =~ ^[0-9]+$ ]] && [[ "$recommended" =~ ^[0-9]+$ ]]; then
                if [[ "$current" -lt "$recommended" ]]; then
                    status="LOW"
                    color="$RED"
                    all_good=false
                fi
            else
                # String comparison for non-numeric values
                if [[ "$current" != "$recommended" ]]; then
                    status="DIFFERENT"
                    color="$YELLOW"
                    all_good=false
                fi
            fi
        fi

        printf "${color}%-45s %-15s %-15s %-10s${NC}\n" \
            "$param" "$current" "$recommended" "$status"
    done

    echo ""
    if $all_good; then
        success "All parameters are optimally configured"
    else
        warning "Some parameters need adjustment - run with 'apply' to fix"
    fi
}

# Backup existing configuration
backup_config() {
    if [[ -f "$SYSCTL_CONF" ]]; then
        local backup
        backup="${SYSCTL_CONF}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$SYSCTL_CONF" "$backup"
        info "Backed up existing config to: $backup"
    fi
}

# Apply tuning parameters
apply_tuning() {
    local force_mode="$1"
    local save_mode="$2"

    if [[ "$save_mode" == "true" ]]; then
        info "Applying development workstation tuning (PERMANENT - will save to config files)..."
    else
        info "Applying development workstation tuning (TEMPORARY - testing only, not saved)..."
    fi
    echo ""

    # Only scan for conflicts if we're saving
    if [[ "$save_mode" == "true" ]]; then
        # Scan for conflicts
        if ! scan_for_conflicts "$force_mode"; then
            if [[ "$force_mode" != "true" ]]; then
                echo ""
                error "Aborting due to conflicts. Use 'apply --force' to override."
            fi
        fi
        echo ""
    fi

    # Apply settings immediately via sysctl
    info "Applying sysctl parameters to running system..."
    for param in "${!SYSCTL_PARAMS[@]}"; do
        local value="${SYSCTL_PARAMS[$param]}"
        if sysctl -w "${param}=${value}" >/dev/null 2>&1; then
            echo -e "${GREEN}  ✓${NC} ${param} = ${value}"
        else
            echo -e "${RED}  ✗${NC} ${param} = ${value} (failed)"
        fi
    done
    echo ""

    # If not saving, we're done
    if [[ "$save_mode" != "true" ]]; then
        warning "Changes applied temporarily - will reset on reboot"
        warning "To make changes permanent, use: apply --save"
        echo ""
        show_status "false"
        return
    fi

    # Save to config files
    info "Saving configuration to persist across reboots..."
    echo ""

    # Backup existing config
    backup_config

    # Create sysctl config
    info "Creating sysctl configuration: $SYSCTL_CONF"
    {
        echo "# Development Workstation Tuning"
        echo "# Generated by linux_development_workstation_tuning.sh"
        echo "# Date: $(date)"
        echo ""
        echo "# This file consolidates development workstation optimizations"
        echo "# Integrated from: 90-memory-optimization.conf, 10-map-count.conf,"
        echo "#                  10-bufferbloat.conf, 10-network-security.conf"
        echo ""

        # Group parameters by category
        echo "# === Inotify Limits ==="
        echo "# Prevents 'too many open files' and file watcher errors"
        echo "# Needed for: IDEs (VS Code, Cursor), build tools, live reload servers"
        for param in "${!SYSCTL_PARAMS[@]}"; do
            if [[ "$param" =~ ^fs\.inotify ]]; then
                # Skip if conflict exists and not in force mode
                if [[ -v "CONFLICTS[$param]" ]] && [[ "$force_mode" != "true" ]]; then
                    echo "# ${param} = ${SYSCTL_PARAMS[$param]}  # SKIPPED - already in ${CONFLICT_FILES[$param]}"
                else
                    echo "${param} = ${SYSCTL_PARAMS[$param]}"
                fi
            fi
        done
        echo ""

        echo "# === File Descriptor Limits ==="
        for param in "${!SYSCTL_PARAMS[@]}"; do
            if [[ "$param" =~ ^fs\.file-max|^fs\.aio ]]; then
                if [[ -v "CONFLICTS[$param]" ]] && [[ "$force_mode" != "true" ]]; then
                    echo "# ${param} = ${SYSCTL_PARAMS[$param]}  # SKIPPED - already in ${CONFLICT_FILES[$param]}"
                else
                    echo "${param} = ${SYSCTL_PARAMS[$param]}"
                fi
            fi
        done
        echo ""

        echo "# === Memory Management ==="
        echo "# Optimized for 31GB development workstation"
        for param in "${!SYSCTL_PARAMS[@]}"; do
            if [[ "$param" =~ ^vm\. ]]; then
                if [[ -v "CONFLICTS[$param]" ]] && [[ "$force_mode" != "true" ]]; then
                    echo "# ${param} = ${SYSCTL_PARAMS[$param]}  # SKIPPED - already in ${CONFLICT_FILES[$param]}"
                else
                    echo "${param} = ${SYSCTL_PARAMS[$param]}"
                fi
            fi
        done
        echo ""

        echo "# === Network Tuning ==="
        echo "# For development servers and build tools"
        for param in "${!SYSCTL_PARAMS[@]}"; do
            if [[ "$param" =~ ^net\. ]]; then
                if [[ -v "CONFLICTS[$param]" ]] && [[ "$force_mode" != "true" ]]; then
                    echo "# ${param} = ${SYSCTL_PARAMS[$param]}  # SKIPPED - already in ${CONFLICT_FILES[$param]}"
                else
                    echo "${param} = ${SYSCTL_PARAMS[$param]}"
                fi
            fi
        done
        echo ""

        echo "# === Shared Memory ==="
        echo "# For containers and databases"
        for param in "${!SYSCTL_PARAMS[@]}"; do
            if [[ "$param" =~ ^kernel\.shm ]]; then
                if [[ -v "CONFLICTS[$param]" ]] && [[ "$force_mode" != "true" ]]; then
                    echo "# ${param} = ${SYSCTL_PARAMS[$param]}  # SKIPPED - already in ${CONFLICT_FILES[$param]}"
                else
                    echo "${param} = ${SYSCTL_PARAMS[$param]}"
                fi
            fi
        done
    } >"$SYSCTL_CONF"

    success "Configuration file created: $SYSCTL_CONF"
    echo ""

    # Create limits.conf for file descriptors
    info "Creating limits configuration: $LIMITS_CONF"
    {
        echo "# Development Workstation Limits"
        echo "# Generated by linux_development_workstation_tuning.sh"
        echo ""
        echo "# File descriptor limits for development tools"
        echo "*    soft    nofile    65536"
        echo "*    hard    nofile    524288"
        echo ""
        echo "# Core dump settings"
        echo "*    soft    core      unlimited"
    } >"$LIMITS_CONF"

    echo ""
    success "Tuning applied successfully!"
    echo ""

    if [[ ${#CONFLICTS[@]} -gt 0 ]] && [[ "$force_mode" != "true" ]]; then
        notice "Some parameters were skipped due to conflicts (see above)"
        notice "To override existing settings, run: sudo $0 apply --force"
        echo ""
    fi

    info "Changes are now active and will persist across reboots"
    echo ""

    # Show new status
    show_status "false"
}

# Reset to system defaults
reset_tuning() {
    info "Resetting to system defaults..."

    if [[ -f "$SYSCTL_CONF" ]]; then
        rm "$SYSCTL_CONF"
        success "Removed $SYSCTL_CONF"
    else
        info "$SYSCTL_CONF does not exist"
    fi

    if [[ -f "$LIMITS_CONF" ]]; then
        rm "$LIMITS_CONF"
        success "Removed $LIMITS_CONF"
    else
        info "$LIMITS_CONF does not exist"
    fi

    echo ""
    warning "System will use default values after reboot or running: sysctl --system"
    echo ""
}

# Main execution
main() {
    local command="${1:-apply}"
    local force_mode="false"
    local save_mode="false"
    local show_all="false"

    # Parse flags
    shift || true
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force)
                force_mode="true"
                shift
                ;;
            --save)
                save_mode="true"
                shift
                ;;
            --all)
                show_all="true"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done

    case "$command" in
        apply)
            check_root
            apply_tuning "$force_mode" "$save_mode"
            ;;
        status)
            show_status "$show_all"
            ;;
        reset | uninstall)
            check_root
            reset_tuning
            ;;
        *)
            error "Unknown command: $command. Use: apply [--save] [--force], status [--all], or reset|uninstall"
            ;;
    esac
}

main "$@"
